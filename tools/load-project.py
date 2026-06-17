#!/usr/bin/env python3
"""
load-project.py — Preprocessore file di progetto per AiAgentFactory.

Scansiona projects/<id>/input/ e converte ogni file non-.md in testo,
producendo input/project-files-context.md che l'orchestratore include
automaticamente come contesto in tutti gli step della pipeline.

Tipi supportati:
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
    try:
        data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    except Exception as e:
        return "", f"Errore lettura immagine: {e}"

    # Stima dimensione: immagini > 5MB potrebbero essere troppo grandi
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > 5:
        return "", f"Immagine troppo grande ({size_mb:.1f} MB) — ridimensiona sotto i 5 MB"

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


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="ID del progetto (cartella in projects/)")
    parser.add_argument(
        "--force", action="store_true",
        help="Rigenera project-files-context.md anche se esiste già",
    )
    parser.add_argument(
        "--no-vision", action="store_true",
        help="Non usare Claude Vision per le immagini (salta con nota)",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Modello Claude per Vision (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    project_dir = PROJECTS_DIR / args.project_id
    if not project_dir.exists():
        print(f"ERRORE: progetto '{args.project_id}' non trovato in {PROJECTS_DIR}/", file=sys.stderr)
        sys.exit(1)

    input_dir = project_dir / "input"
    if not input_dir.exists():
        print(f"ERRORE: cartella input/ non trovata in {project_dir}", file=sys.stderr)
        sys.exit(1)

    output_file = input_dir / OUTPUT_FILE
    if output_file.exists() and not args.force:
        print(f"  ℹ  {output_file} già presente.")
        print("     Usa --force per rigenerarlo.")
        sys.exit(0)

    # Raccogli file non-.md nella cartella input/ (non ricorsivo)
    candidates = sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() != ".md" and p.name != OUTPUT_FILE
    )

    if not candidates:
        print(f"  ℹ  Nessun file da processare in {input_dir}")
        print("     Aggiungi PDF, immagini o file di testo nella cartella input/.")
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
