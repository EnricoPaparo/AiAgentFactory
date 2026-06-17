#!/usr/bin/env python3
"""
AISA — AISolutionArchitect

Trasforma un'idea in qualsiasi formato in tre documenti professionali:
  - Analisi dei Requisiti
  - Architettura
  - Piano di Implementazione

Uso:
  python tools/run.py "descrizione del progetto"
  python tools/run.py "descrizione" --files ./miei-documenti/
  python tools/run.py "descrizione" --files ./docs/ --model claude-opus-4-8
  python tools/run.py "descrizione" --files ./docs/ --budget 3.00
  python tools/run.py "descrizione" --files ./docs/ --review        # gate interattivo tra step
  python tools/run.py "descrizione" --dry-run                        # anteprima senza eseguire
"""

import os
import sys
import re
import json
import shutil
import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERRORE: installa le dipendenze con: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

REPO_ROOT    = Path(__file__).parent.parent
AGENTS_DIR   = REPO_ROOT / "agents"
PROJECTS_DIR = REPO_ROOT / "projects"
DEFAULT_MODEL = "claude-opus-4-8"
MAX_TOOL_CALLS = 30

TEXT_EXTENSIONS = {
    ".txt", ".md", ".pdf", ".docx",
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb",
    ".json", ".yaml", ".yml", ".toml", ".xml", ".html", ".htm",
    ".csv", ".sql", ".sh", ".cs", ".cpp", ".c", ".h",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

TOOLS = [
    {
        "name": "read_file",
        "description": "Leggi il contenuto di un file. Usa percorsi relativi alla root del repo o al workspace di progetto.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Percorso del file da leggere"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Scrivi contenuto in un file nel workspace di progetto. Crea le directory necessarie automaticamente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Percorso del file (relativo al workspace di progetto)"},
                "content": {"type": "string", "description": "Contenuto da scrivere"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "complete_step",
        "description": "Segnala il completamento di questo step con un riepilogo dei file prodotti.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Riepilogo di cosa è stato fatto"},
                "files_produced": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista dei file prodotti"
                }
            },
            "required": ["summary", "files_produced"]
        }
    }
]


def die(msg: str) -> None:
    print(f"\nERRORE: {msg}", file=sys.stderr)
    sys.exit(1)


def kebab(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return re.sub(r"-+", "-", slug)[:64] or "aisa-project"


def read_file_safe(path: Path, project: Path) -> str:
    candidates = [
        project / path,
        REPO_ROOT / path,
        Path(path),
    ]
    for p in candidates:
        try:
            resolved = p.resolve()
            if resolved.exists() and resolved.is_file():
                return resolved.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass
    return f"[FILE NON TROVATO: {path}]"


def write_file_safe(path: Path, content: str, project: Path) -> str:
    # Blocca path traversal fuori dal workspace
    try:
        target = (project / path).resolve()
        project_resolved = project.resolve()
        if not str(target).startswith(str(project_resolved)):
            return f"ERRORE: scrittura fuori dal workspace non permessa: {path}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Scritto: {target.relative_to(project)}"
    except Exception as e:
        return f"ERRORE scrittura {path}: {e}"


def handle_tool(name: str, inputs: dict, project: Path) -> str:
    if name == "read_file":
        return read_file_safe(Path(inputs["path"]), project)
    if name == "write_file":
        return write_file_safe(Path(inputs["path"]), inputs["content"], project)
    if name == "complete_step":
        return json.dumps({"status": "completed", "summary": inputs.get("summary", ""), "files": inputs.get("files_produced", [])})
    return f"ERRORE: tool sconosciuto: {name}"


def load_input_files(files_path: Path, project: Path) -> str:
    """Carica e consolida tutti i file di input in un unico blocco testo."""
    input_dir = project / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    if files_path.is_dir():
        sources = sorted(files_path.iterdir())
    else:
        sources = [files_path]

    parts = []
    copied = 0
    for src in sources:
        if not src.is_file():
            continue
        dest = input_dir / src.name
        shutil.copy2(src, dest)
        copied += 1

        ext = src.suffix.lower()
        if ext in TEXT_EXTENSIONS:
            try:
                text = src.read_text(encoding="utf-8", errors="replace")
                parts.append(f"### {src.name}\n\n{text}")
            except Exception:
                parts.append(f"### {src.name}\n\n[Impossibile leggere il file]")
        elif ext in IMAGE_EXTENSIONS:
            parts.append(f"### {src.name}\n\n[Immagine — verrà descritta dall'agente se necessario]")

    if copied:
        print(f"  {copied} file caricati da {files_path}")
    return "\n\n---\n\n".join(parts) if parts else ""


def run_agent(
    client: anthropic.Anthropic,
    model: str,
    step_name: str,
    agent_file: Path,
    context: str,
    project: Path,
    review_mode: bool,
) -> dict:
    """Esegue un singolo agente e restituisce il risultato."""
    agent_prompt = agent_file.read_text(encoding="utf-8")

    system = f"""{agent_prompt}

---

## Workspace del progetto

Il tuo workspace è: {project}
Tutti i file che scrivi devono essere relativi a questo workspace.

## Istruzioni operative

1. Leggi tutto il contesto fornito.
2. Se hai bisogno di leggere file aggiuntivi usa il tool `read_file`.
3. Quando hai completato il tuo documento, scrivilo con `write_file`.
4. Chiudi sempre con `complete_step` per segnalare il completamento.
"""

    user_message = f"""## Contesto del progetto

{context}

---

Esegui il tuo ruolo e produci il documento richiesto nel workspace del progetto.
"""

    messages = [{"role": "user", "content": user_message}]
    tool_calls = 0
    result = {"status": "running", "files": [], "summary": ""}

    print(f"  → {step_name}...", end="", flush=True)

    while tool_calls < MAX_TOOL_CALLS:
        response = client.messages.create(
            model=model,
            max_tokens=8192,
            system=system,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                tool_calls += 1
                tool_output = handle_tool(block.name, block.input, project)

                if block.name == "complete_step":
                    try:
                        data = json.loads(tool_output)
                        result["status"] = "completed"
                        result["files"] = data.get("files", [])
                        result["summary"] = data.get("summary", "")
                    except Exception:
                        result["status"] = "completed"

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": tool_output,
                })

        if response.stop_reason == "end_turn" and not tool_results:
            if result["status"] != "completed":
                result["status"] = "completed"
            break

        if tool_results:
            messages.append({"role": "user", "content": tool_results})

        if result["status"] == "completed":
            break

    print(f" ✓")
    return result


def build_context(description: str, input_content: str, prev_docs: dict) -> str:
    parts = [f"## Descrizione del progetto\n\n{description}"]
    if input_content:
        parts.append(f"## Materiali forniti dall'utente\n\n{input_content}")
    for doc_name, doc_path in prev_docs.items():
        if doc_path.exists():
            parts.append(f"## {doc_name}\n\n{doc_path.read_text(encoding='utf-8')}")
    return "\n\n---\n\n".join(parts)


def human_gate(step_name: str) -> bool:
    """Gate interattivo tra step. Restituisce True se approvato."""
    print(f"\n{'─'*60}")
    print(f"  GATE — {step_name} completato")
    print(f"  Rivedi il documento prodotto prima di continuare.")
    print(f"{'─'*60}")
    while True:
        choice = input("  Continuare? [s=sì / n=no]: ").strip().lower()
        if choice in ("s", "si", "sì", "y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("  Risposta non valida. Digita 's' per continuare o 'n' per fermare.")


def cmd_run(args: argparse.Namespace) -> None:
    description = args.description.strip()
    if not description:
        die("la descrizione del progetto non può essere vuota")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key and not args.dry_run:
        die("variabile ANTHROPIC_API_KEY non impostata.\nEsempio: export ANTHROPIC_API_KEY=sk-ant-...")

    project_id = args.project_id or kebab(description)
    project = PROJECTS_DIR / project_id

    if project.exists() and not args.force:
        die(f"workspace '{project_id}' esiste già. Usa --force per sovrascrivere.")

    project.mkdir(parents=True, exist_ok=True)
    (project / "documents").mkdir(exist_ok=True)
    (project / "input").mkdir(exist_ok=True)

    print(f"\nAISA — AISolutionArchitect")
    print(f"{'─'*60}")
    print(f"  Progetto : {project_id}")
    print(f"  Modello  : {args.model}")
    print(f"  Workspace: {project}")
    print(f"{'─'*60}\n")

    # Carica file di input
    input_content = ""
    if args.files:
        src = Path(args.files)
        if not src.exists():
            die(f"percorso non trovato: {args.files}")
        input_content = load_input_files(src, project)

    if args.dry_run:
        print("[DRY RUN] Passi che verrebbero eseguiti:")
        print("  1. Requirement Analyst → documents/requirements.md")
        print("  2. Architect           → documents/architecture.md")
        print("  3. Implementation Planner → documents/implementation-plan.md")
        print("  4. Generazione PDF     → documents/*.pdf")
        print("\nNessuna chiamata API effettuata.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    model  = args.model
    start  = time.time()

    steps = [
        {
            "name": "Requirement Analyst",
            "agent": AGENTS_DIR / "requirement-analyst" / "requirement-analyst.md",
            "prev_docs": {},
            "output": project / "documents" / "requirements.md",
        },
        {
            "name": "Architect",
            "agent": AGENTS_DIR / "architect" / "architect.md",
            "prev_docs": {"Analisi dei Requisiti": project / "documents" / "requirements.md"},
            "output": project / "documents" / "architecture.md",
        },
        {
            "name": "Implementation Planner",
            "agent": AGENTS_DIR / "implementation-planner" / "implementation-planner.md",
            "prev_docs": {
                "Analisi dei Requisiti": project / "documents" / "requirements.md",
                "Architettura": project / "documents" / "architecture.md",
            },
            "output": project / "documents" / "implementation-plan.md",
        },
    ]

    for i, step in enumerate(steps):
        print(f"[{i+1}/{len(steps)}] {step['name']}")
        context = build_context(description, input_content, step["prev_docs"])
        result  = run_agent(client, model, step["name"], step["agent"], context, project, args.review)

        if not step["output"].exists():
            print(f"  ⚠ Documento non trovato: {step['output']}")
        else:
            size = step["output"].stat().st_size
            print(f"  ✓ {step['output'].name} ({size:,} bytes)")

        if args.review and i < len(steps) - 1:
            if not human_gate(step["name"]):
                print("\nPipeline interrotta dall'utente.")
                sys.exit(0)
        print()

    elapsed = time.time() - start
    print(f"{'─'*60}")
    print(f"  Completato in {elapsed:.0f}s")
    print(f"  Documenti in: {project / 'documents'}/")
    print(f"{'─'*60}")

    # Genera PDF se disponibile
    pdf_script = REPO_ROOT / "tools" / "pdf.py"
    if pdf_script.exists():
        print("\nGenerazione PDF...")
        subprocess.run([sys.executable, str(pdf_script), str(project)], check=False)
    else:
        print("\nGenerazione PDF: installa WeasyPrint e crea tools/pdf.py per abilitarla.")

    print(f"\nDone. Documenti pronti in:\n  {project / 'documents'}/\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="aisa",
        description="AISA — trasforma un'idea in tre documenti professionali",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("description", help="descrizione del progetto (in virgolette)")
    parser.add_argument("--files", "-f", metavar="PERCORSO",
                        help="file o cartella con materiali di input")
    parser.add_argument("--project-id", metavar="ID",
                        help="ID workspace (default: auto-generato dalla descrizione)")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, metavar="MODELLO",
                        help=f"modello AI (default: {DEFAULT_MODEL})")
    parser.add_argument("--budget", "-b", type=float, metavar="USD",
                        help="budget massimo in USD (non ancora implementato)")
    parser.add_argument("--review", action="store_true",
                        help="attiva gate di revisione interattivo tra ogni step")
    parser.add_argument("--dry-run", action="store_true",
                        help="mostra i passi senza eseguire chiamate API")
    parser.add_argument("--force", action="store_true",
                        help="sovrascrive workspace esistente")
    parser.set_defaults(func=cmd_run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
