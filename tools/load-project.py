#!/usr/bin/env python3
"""
load-project.py — Preprocessore file di progetto per AiAgentFactory.

Scansiona projects/<id>/input/ e converte ogni file non-.md in testo,
producendo input/project-files-context.md che l'orchestratore include
automaticamente come contesto in tutti gli step della pipeline.

Con --from-repo scansiona un codebase esistente e produce
input/existing-codebase.md con struttura e contenuto dei file sorgente.

Tipi supportati (input/):
  - Testo  : .txt .py .js .ts .jsx .tsx .java .go .rb .php .cs .cpp .c .h
             .json .yaml .yml .toml .xml .html .htm .css .scss .md .csv .sql
  - PDF    : .pdf  (richiede: pip install pypdf)
  - Immagini: .png .jpg .jpeg .webp .gif  (richiede ANTHROPIC_API_KEY)
  - Word   : .docx  (richiede: pip install python-docx)
  - Audio  : .mp3 .wav .m4a .ogg → non supportato, mostra istruzioni

Uso:
  python tools/load-project.py <project-id>
  python tools/load-project.py <project-id> --force
  python tools/load-project.py <project-id> --model claude-haiku-4-5
  python tools/load-project.py <project-id> --no-vision
  python tools/load-project.py <project-id> --from-repo /path/to/repo
  python tools/load-project.py <project-id> --from-repo /path/to/repo --max-repo-chars 200000
"""

import os
import sys
import base64
import argparse
from datetime import datetime
from pathlib import Path

PROJECTS_DIR = Path("projects")
OUTPUT_FILE  = "project-files-context.md"
DEFAULT_MODEL = "claude-haiku-4-5"

TEXT_EXTENSIONS = {
    ".txt", ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb",
    ".php", ".cs", ".cpp", ".c", ".h", ".hpp", ".rs", ".swift", ".kt",
    ".json", ".yaml", ".yml", ".toml", ".xml", ".html", ".htm", ".css",
    ".scss", ".sass", ".less", ".csv", ".sql", ".sh", ".bat", ".ps1",
    ".env", ".ini", ".cfg", ".conf", ".dockerfile", ".makefile",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"}

# ── Costanti per --from-repo ───────────────────────────────────────────────────

REPO_SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", "dist", "build", ".next", ".nuxt",
    "venv", ".venv", "env", ".env", "target", ".gradle", ".idea", ".vscode",
    "coverage", ".nyc_output", ".pytest_cache", ".mypy_cache", "out", ".output",
    ".turbo", ".cache", "vendor", ".tox", "htmlcov", "eggs", ".eggs",
    "buck-out", ".buck", "CMakeFiles", "Pods",
}

REPO_SKIP_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".class", ".jar", ".war", ".ear",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".wasm", ".obj", ".o",
    ".map", ".min.js", ".min.css",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".tiff",
    ".pdf", ".docx", ".xlsx", ".pptx",
    ".zip", ".tar", ".gz", ".rar", ".7z", ".dmg", ".iso",
    ".db", ".sqlite", ".sqlite3",
    ".log", ".lock",
}

# File di configurazione/manifesto: inclusi per primi indipendentemente dalla dimensione
REPO_PRIORITY_FILES = {
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "requirements.txt", "requirements-dev.txt", "pyproject.toml",
    "setup.py", "setup.cfg", "Pipfile", "Pipfile.lock",
    "go.mod", "go.sum",
    "Cargo.toml",
    "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle",
    "tsconfig.json", "jsconfig.json", ".eslintrc.json", ".eslintrc.js",
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    ".env.example", ".env.sample",
    "Makefile", "makefile",
    "README.md", "ARCHITECTURE.md", "CONTRIBUTING.md",
}

# Mappa estensione → linguaggio per i blocchi markdown
_LANG_MAP = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".jsx": "jsx", ".tsx": "tsx", ".java": "java", ".go": "go",
    ".rb": "ruby", ".php": "php", ".cs": "csharp", ".cpp": "cpp",
    ".c": "c", ".h": "c", ".rs": "rust", ".swift": "swift",
    ".kt": "kotlin", ".scala": "scala", ".sh": "bash", ".bat": "bat",
    ".ps1": "powershell", ".json": "json", ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml", ".xml": "xml", ".html": "html", ".htm": "html",
    ".css": "css", ".scss": "scss", ".sql": "sql", ".md": "markdown",
    ".dockerfile": "dockerfile",
}

REPO_MAX_FILE_CHARS  = 12_000   # tronca file singolo oltre questa soglia
REPO_DEFAULT_MAX_CHARS = 150_000  # limite totale caratteri aggregati


# ── Handler testo ──────────────────────────────────────────────────────────────

def load_text(path: Path) -> tuple[str, str]:
    """Ritorna (contenuto, nota). nota è vuota se ok."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > 60_000:
            text = text[:60_000] + f"\n\n[... troncato: {len(text):,} caratteri totali]"
        return text, ""
    except Exception as e:
        return "", f"Errore lettura: {e}"


# ── Handler PDF ────────────────────────────────────────────────────────────────

def load_pdf(path: Path) -> tuple[str, str]:
    try:
        import pypdf
    except ImportError:
        return "", "pypdf non installato — esegui: pip install pypdf"
    try:
        reader = pypdf.PdfReader(str(path))
        pages = []
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[Pagina {i}]\n{text.strip()}")
        if not pages:
            return "", "Nessun testo estraibile (PDF scansionato o solo immagini)"
        full = "\n\n".join(pages)
        if len(full) > 60_000:
            full = full[:60_000] + f"\n\n[... troncato: {len(full):,} caratteri totali]"
        return full, f"{len(reader.pages)} pagine"
    except Exception as e:
        return "", f"Errore lettura PDF: {e}"


# ── Handler DOCX ───────────────────────────────────────────────────────────────

def load_docx(path: Path) -> tuple[str, str]:
    try:
        from docx import Document
    except ImportError:
        return "", "python-docx non installato — esegui: pip install python-docx"
    try:
        doc = Document(str(path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        text = "\n\n".join(paragraphs)
        if len(text) > 60_000:
            text = text[:60_000] + f"\n\n[... troncato: {len(text):,} caratteri totali]"
        return text, f"{len(paragraphs)} paragrafi"
    except Exception as e:
        return "", f"Errore lettura DOCX: {e}"


# ── Handler immagini (Claude Vision) ──────────────────────────────────────────

_MEDIA_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif",
}

def load_image(path: Path, model: str) -> tuple[str, str]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "", "ANTHROPIC_API_KEY non impostata — descrizione immagine non disponibile"
    try:
        import anthropic
    except ImportError:
        return "", "anthropic non installato — esegui: pip install anthropic"

    media_type = _MEDIA_TYPES.get(path.suffix.lower(), "image/png")

    # Controlla dimensione PRIMA di leggere il file
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > 5:
        return "", f"Immagine troppo grande ({size_mb:.1f} MB) — ridimensiona sotto i 5 MB"

    try:
        data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    except Exception as e:
        return "", f"Errore lettura immagine: {e}"

    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": data,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "Descrivi questa immagine come contesto per un progetto software. "
                            "Includi: tipo di documento o schermata, contenuti visibili "
                            "(testo, layout, dati, diagrammi), informazioni rilevanti per "
                            "un team di sviluppo. Sii preciso e conciso."
                        ),
                    },
                ],
            }],
        )
        description = response.content[0].text
        return description, f"descritto via Claude Vision ({model})"
    except Exception as e:
        return "", f"Errore Claude Vision: {e}"


# ── Processore principale ──────────────────────────────────────────────────────

def process_file(path: Path, model: str, no_vision: bool) -> dict:
    ext = path.suffix.lower()
    size_kb = path.stat().st_size // 1024

    if ext in TEXT_EXTENSIONS or ext == "":
        content, note = load_text(path)
        kind = "Testo"
    elif ext == ".pdf":
        content, note = load_pdf(path)
        kind = "PDF"
    elif ext == ".docx":
        content, note = load_docx(path)
        kind = "Word"
    elif ext in IMAGE_EXTENSIONS:
        if no_vision:
            content, note = "", "Vision disabilitata (--no-vision)"
        else:
            content, note = load_image(path, model)
        kind = "Immagine"
    elif ext in AUDIO_EXTENSIONS:
        content = ""
        note = (
            "Formato audio non supportato. "
            "Trascrivi manualmente e salva come .txt nella cartella input/."
        )
        kind = "Audio"
    else:
        content = ""
        note = f"Formato '{ext}' non supportato."
        kind = "Sconosciuto"

    return {
        "path": path,
        "name": path.name,
        "kind": kind,
        "size_kb": size_kb,
        "content": content,
        "note": note,
        "ok": bool(content),
    }


def build_context_file(results: list[dict], project_id: str) -> str:
    lines = [
        "# Project Files Context",
        "",
        f"Progetto: {project_id}",
        f"Generato: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"File processati: {len(results)}",
        "",
    ]

    ok     = [r for r in results if r["ok"]]
    skipped = [r for r in results if not r["ok"]]

    if ok:
        lines += ["---", ""]
        for r in ok:
            note_str = f"  _{r['note']}_" if r["note"] else ""
            lines += [
                f"## {r['name']}  ({r['kind']}, {r['size_kb']} KB){note_str}",
                "",
                r["content"],
                "",
            ]

    if skipped:
        lines += ["---", "", "## File saltati", ""]
        for r in skipped:
            lines.append(f"- **{r['name']}** ({r['kind']}, {r['size_kb']} KB) — {r['note']}")
        lines.append("")

    return "\n".join(lines)


# ── Repo scanner (--from-repo) ────────────────────────────────────────────────

def _collect_repo_files(repo_root: Path) -> tuple[list[Path], int]:
    """
    Visita ricorsivamente repo_root saltando directory e file irrilevanti.
    Ritorna (lista_file_ordinata, totale_file_scansionati).
    """
    all_files: list[Path] = []
    total_scanned = 0

    for dirpath, dirnames, filenames in os.walk(repo_root):
        current = Path(dirpath)
        # Rimuovi in-place le dir da saltare (os.walk non le visiterà)
        dirnames[:] = [
            d for d in dirnames
            if d not in REPO_SKIP_DIRS and not d.startswith(".")
        ]
        for fname in filenames:
            total_scanned += 1
            fpath = current / fname
            if fpath.suffix.lower() in REPO_SKIP_EXTENSIONS:
                continue
            if fname.startswith(".") and fname not in {
                ".env.example", ".env.sample", ".gitignore", ".editorconfig"
            }:
                continue
            all_files.append(fpath)

    # Priorità: manifest/config prima, poi resto ordinato per percorso
    priority = [f for f in all_files if f.name in REPO_PRIORITY_FILES]
    rest     = sorted([f for f in all_files if f.name not in REPO_PRIORITY_FILES],
                      key=lambda p: str(p))
    return priority + rest, total_scanned


def _build_dir_tree(repo_root: Path, files: list[Path], max_entries: int = 200) -> str:
    """Genera un albero di directory compatto (stile find) dei file inclusi."""
    rel_paths = sorted(str(f.relative_to(repo_root)).replace("\\", "/") for f in files)
    if len(rel_paths) > max_entries:
        shown = rel_paths[:max_entries]
        hidden = len(rel_paths) - max_entries
        lines = shown + [f"... e altri {hidden} file"]
    else:
        lines = rel_paths
    return "\n".join(f"  {p}" for p in lines)


def load_from_repo(repo_path: Path, max_total_chars: int = REPO_DEFAULT_MAX_CHARS) -> str:
    """
    Scansiona un codebase esistente e restituisce il contenuto markdown
    da scrivere in input/existing-codebase.md.
    """
    repo_path = repo_path.resolve()
    if not repo_path.exists():
        raise FileNotFoundError(f"Repository non trovato: {repo_path}")

    print(f"\n  Scansione repo: {repo_path}")
    print(f"  {'─'*50}")

    ordered_files, total_scanned = _collect_repo_files(repo_path)

    # Leggi i file fino al limite totale
    sections_config: list[str] = []
    sections_source: list[str] = []
    included_files:  list[Path] = []
    skipped_large:   list[str]  = []
    skipped_limit:   int        = 0
    total_chars      = 0

    for fpath in ordered_files:
        if total_chars >= max_total_chars:
            skipped_limit += 1
            continue

        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        rel      = str(fpath.relative_to(repo_path)).replace("\\", "/")
        ext      = fpath.suffix.lower()
        lang     = _LANG_MAP.get(ext, "")
        original = len(content)

        if original > REPO_MAX_FILE_CHARS:
            skipped_large.append(f"{rel} ({original:,} chars)")
            content = content[:REPO_MAX_FILE_CHARS] + f"\n... [troncato — {original:,} chars totali]"

        section = f"### {rel}\n```{lang}\n{content}\n```\n"
        total_chars += len(content)
        included_files.append(fpath)

        if fpath.name in REPO_PRIORITY_FILES:
            sections_config.append(section)
        else:
            sections_source.append(section)

        icon = "✓" if original <= REPO_MAX_FILE_CHARS else "~"
        print(f"  {icon} {rel}")

    # Assembla documento
    tree = _build_dir_tree(repo_path, included_files)

    lines = [
        "# Existing Codebase",
        "",
        f"Repository: {repo_path}",
        f"Generato: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"File inclusi: {len(included_files)} / {total_scanned} scansionati",
        f"Caratteri totali: {total_chars:,} / {max_total_chars:,}",
        "",
        "---",
        "",
        "## Struttura",
        "",
        tree,
        "",
    ]

    if skipped_large:
        lines += [
            "## File troncati (oltre 12k chars — usa read_file per leggere intero)",
            "",
        ]
        for s in skipped_large:
            lines.append(f"- {s}")
        lines.append("")

    if skipped_limit:
        lines += [
            f"> ℹ {skipped_limit} file saltati per limite totale ({max_total_chars:,} chars).",
            "> Usa --max-repo-chars per aumentare il limite.",
            "",
        ]

    if sections_config:
        lines += ["---", "", "## Configurazione e manifesti", ""]
        lines.extend(sections_config)

    if sections_source:
        lines += ["---", "", "## Codice sorgente", ""]
        lines.extend(sections_source)

    return "\n".join(lines)


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="ID del progetto (cartella in projects/)")
    parser.add_argument(
        "--force", action="store_true",
        help="Rigenera i file di contesto anche se esistono già",
    )
    parser.add_argument(
        "--no-vision", action="store_true",
        help="Non usare Claude Vision per le immagini (salta con nota)",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Modello Claude per Vision (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--from-repo", metavar="PATH", dest="from_repo",
        help=(
            "Importa un codebase esistente: scansiona PATH e produce "
            "input/existing-codebase.md con struttura e contenuto dei file sorgente."
        ),
    )
    parser.add_argument(
        "--max-repo-chars", type=int, default=REPO_DEFAULT_MAX_CHARS, metavar="N",
        help=f"Limite totale caratteri per --from-repo (default: {REPO_DEFAULT_MAX_CHARS:,})",
    )
    args = parser.parse_args()

    project_dir = PROJECTS_DIR / args.project_id
    if not project_dir.exists():
        print(f"ERRORE: progetto '{args.project_id}' non trovato in {PROJECTS_DIR}/", file=sys.stderr)
        sys.exit(1)

    input_dir = project_dir / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    # ── Modalità --from-repo ───────────────────────────────────────────────────
    if args.from_repo:
        repo_output = input_dir / "existing-codebase.md"
        if repo_output.exists() and not args.force:
            print(f"  ℹ  {repo_output} già presente.")
            print("     Usa --force per rigenerarlo.")
        else:
            try:
                context = load_from_repo(Path(args.from_repo), args.max_repo_chars)
                repo_output.write_text(context, encoding="utf-8")
                size_kb = repo_output.stat().st_size // 1024
                print(f"\n  {'─'*50}")
                print(f"  ✓ {repo_output}  ({size_kb} KB)")
                print(f"\n  Prossimo step:")
                print(f"    python tools/orchestrate.py {args.project_id}\n")
            except FileNotFoundError as e:
                print(f"ERRORE: {e}", file=sys.stderr)
                sys.exit(1)
        return

    # ── Modalità normale: file in input/ ──────────────────────────────────────
    output_file = input_dir / OUTPUT_FILE
    if output_file.exists() and not args.force:
        print(f"  ℹ  {output_file} già presente.")
        print("     Usa --force per rigenerarlo.")
        sys.exit(0)

    candidates = sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() != ".md" and p.name != OUTPUT_FILE
    )

    if not candidates:
        print(f"  ℹ  Nessun file da processare in {input_dir}")
        print("     Aggiungi PDF, immagini o file di testo nella cartella input/.")
        print("     Oppure usa --from-repo /path/to/repo per importare un codebase.")
        sys.exit(0)

    print(f"\n  Project Input Loader — {args.project_id}")
    print(f"  {'─'*50}")
    print(f"  File trovati: {len(candidates)}\n")

    results = []
    for path in candidates:
        print(f"  → {path.name} ", end="", flush=True)
        result = process_file(path, args.model, args.no_vision)
        results.append(result)
        if result["ok"]:
            note = f"  ({result['note']})" if result["note"] else ""
            print(f"✓ {result['kind']}{note}")
        else:
            print(f"✗ saltato — {result['note']}")

    context = build_context_file(results, args.project_id)
    output_file.write_text(context, encoding="utf-8")

    ok_count = sum(1 for r in results if r["ok"])
    print(f"\n  {'─'*50}")
    print(f"  ✓ {output_file}")
    print(f"    {ok_count}/{len(results)} file inclusi nel contesto")
    print(f"\n  Prossimo step:")
    print(f"    python tools/orchestrate.py {args.project_id}\n")


if __name__ == "__main__":
    main()
