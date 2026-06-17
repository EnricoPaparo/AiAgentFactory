#!/usr/bin/env python3
"""
AISA — Generatore PDF professionale

Converte i documenti Markdown prodotti dalla pipeline in PDF con:
- Copertina con titolo, data, versione
- Indice automatico
- Header/footer per pagina
- Tipografia pulita e leggibile

Uso:
  python tools/pdf.py <project-workspace>
  python tools/pdf.py projects/mio-progetto
  python tools/pdf.py projects/mio-progetto --output ./output/
"""

import sys
import argparse
import re
from datetime import datetime
from pathlib import Path

try:
    import markdown as md_lib
except ImportError:
    print("ERRORE: installa le dipendenze con: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    from weasyprint import HTML as WeasyprintHTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_OK = True
except ImportError:
    WEASYPRINT_OK = False


DOCUMENT_META = {
    "requirements": {
        "title": "Analisi dei Requisiti",
        "subtitle": "Requirements Analysis Document",
        "accent": "#1a56a0",
        "icon": "📋",
    },
    "architecture": {
        "title": "Architettura del Sistema",
        "subtitle": "Architecture Design Document",
        "accent": "#0f7b5a",
        "icon": "🏗",
    },
    "implementation-plan": {
        "title": "Piano di Implementazione",
        "subtitle": "Implementation Plan Document",
        "accent": "#7b3f0f",
        "icon": "📅",
    },
}

CSS_TEMPLATE = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {{
  --accent: {accent};
  --accent-light: {accent}18;
  --text: #1a1a2e;
  --muted: #6b7280;
  --border: #e5e7eb;
  --bg-code: #f8fafc;
}}

@page {{
  size: A4;
  margin: 20mm 18mm 22mm 18mm;

  @top-left {{
    content: "{project_name}";
    font-family: 'Inter', sans-serif;
    font-size: 8pt;
    color: var(--muted);
  }}
  @top-right {{
    content: "{doc_title}";
    font-family: 'Inter', sans-serif;
    font-size: 8pt;
    color: var(--muted);
  }}
  @bottom-center {{
    content: counter(page) " / " counter(pages);
    font-family: 'Inter', sans-serif;
    font-size: 8pt;
    color: var(--muted);
  }}
}}

@page :first {{
  @top-left {{ content: ""; }}
  @top-right {{ content: ""; }}
  @bottom-center {{ content: ""; }}
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: 'Inter', -apple-system, sans-serif;
  font-size: 10pt;
  line-height: 1.65;
  color: var(--text);
  background: white;
}}

/* ── COPERTINA ─────────────────────────────────────────────── */

.cover {{
  page-break-after: always;
  min-height: 257mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0;
}}

.cover-header {{
  background: var(--accent);
  padding: 32px 36px 28px;
  color: white;
}}

.cover-brand {{
  font-size: 11pt;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.85;
  margin-bottom: 40px;
}}

.cover-title {{
  font-size: 28pt;
  font-weight: 700;
  line-height: 1.15;
  margin-bottom: 8px;
}}

.cover-subtitle {{
  font-size: 12pt;
  opacity: 0.75;
  font-weight: 400;
}}

.cover-body {{
  flex: 1;
  padding: 36px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}}

.cover-project {{
  border-left: 4px solid var(--accent);
  padding: 14px 18px;
  background: var(--accent-light);
  border-radius: 0 6px 6px 0;
}}

.cover-project-label {{
  font-size: 8pt;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  margin-bottom: 4px;
}}

.cover-project-name {{
  font-size: 14pt;
  font-weight: 600;
  color: var(--text);
}}

.cover-meta {{
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
}}

.cover-meta-item {{
  display: flex;
  flex-direction: column;
  gap: 2px;
}}

.cover-meta-label {{
  font-size: 7.5pt;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}}

.cover-meta-value {{
  font-size: 10pt;
  font-weight: 500;
  color: var(--text);
}}

.cover-footer {{
  border-top: 1px solid var(--border);
  padding: 16px 36px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}

.cover-footer-brand {{
  font-size: 9pt;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.05em;
}}

.cover-footer-note {{
  font-size: 8pt;
  color: var(--muted);
}}

/* ── CONTENUTO ─────────────────────────────────────────────── */

.content {{
  padding-top: 4mm;
}}

h1 {{
  font-size: 18pt;
  font-weight: 700;
  color: var(--accent);
  margin-top: 28px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--accent);
  page-break-after: avoid;
}}

h1:first-child {{
  margin-top: 0;
}}

h2 {{
  font-size: 13pt;
  font-weight: 600;
  color: var(--text);
  margin-top: 22px;
  margin-bottom: 8px;
  page-break-after: avoid;
}}

h3 {{
  font-size: 11pt;
  font-weight: 600;
  color: var(--text);
  margin-top: 16px;
  margin-bottom: 6px;
  page-break-after: avoid;
}}

h4 {{
  font-size: 10pt;
  font-weight: 600;
  color: var(--muted);
  margin-top: 12px;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  page-break-after: avoid;
}}

p {{
  margin-bottom: 8px;
}}

ul, ol {{
  margin: 6px 0 10px 20px;
}}

li {{
  margin-bottom: 4px;
}}

li > ul, li > ol {{
  margin-top: 3px;
  margin-bottom: 3px;
}}

strong {{
  font-weight: 600;
  color: var(--text);
}}

em {{
  font-style: italic;
}}

code {{
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  font-size: 8.5pt;
  background: var(--bg-code);
  border: 1px solid var(--border);
  padding: 1px 5px;
  border-radius: 3px;
}}

pre {{
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 12px 14px;
  margin: 10px 0;
  overflow: hidden;
  page-break-inside: avoid;
}}

pre code {{
  background: none;
  border: none;
  padding: 0;
  font-size: 8pt;
  line-height: 1.5;
}}

/* ── TABELLE ───────────────────────────────────────────────── */

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 9pt;
  page-break-inside: avoid;
}}

thead {{
  background: var(--accent);
  color: white;
}}

thead th {{
  padding: 8px 10px;
  text-align: left;
  font-weight: 600;
  font-size: 8.5pt;
  letter-spacing: 0.03em;
}}

tbody tr:nth-child(even) {{
  background: var(--accent-light);
}}

tbody td {{
  padding: 7px 10px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}}

/* ── BLOCCHI SPECIALI ──────────────────────────────────────── */

blockquote {{
  border-left: 3px solid var(--accent);
  background: var(--accent-light);
  padding: 10px 14px;
  margin: 10px 0;
  border-radius: 0 4px 4px 0;
  font-size: 9.5pt;
  page-break-inside: avoid;
}}

hr {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 20px 0;
}}

/* ── CHECKLIST ─────────────────────────────────────────────── */

.task-list-item {{
  list-style: none;
  margin-left: -16px;
}}

input[type="checkbox"] {{
  margin-right: 6px;
  accent-color: var(--accent);
}}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <style>{css}</style>
</head>
<body>

<div class="cover">
  <div class="cover-header">
    <div class="cover-brand">AISA · AISolutionArchitect</div>
    <div class="cover-title">{doc_title}</div>
    <div class="cover-subtitle">{doc_subtitle}</div>
  </div>
  <div class="cover-body">
    <div class="cover-project">
      <div class="cover-project-label">Progetto</div>
      <div class="cover-project-name">{project_name}</div>
    </div>
    <div class="cover-meta">
      <div class="cover-meta-item">
        <span class="cover-meta-label">Data</span>
        <span class="cover-meta-value">{date}</span>
      </div>
      <div class="cover-meta-item">
        <span class="cover-meta-label">Versione</span>
        <span class="cover-meta-value">{version}</span>
      </div>
      <div class="cover-meta-item">
        <span class="cover-meta-label">Documento</span>
        <span class="cover-meta-value">{doc_id}</span>
      </div>
    </div>
  </div>
  <div class="cover-footer">
    <span class="cover-footer-brand">AISA</span>
    <span class="cover-footer-note">Generato automaticamente · Riservato</span>
  </div>
</div>

<div class="content">
{body}
</div>

</body>
</html>"""


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def md_to_html(text: str) -> str:
    extensions = [
        "tables",
        "fenced_code",
        "attr_list",
        "def_list",
        "footnotes",
        "toc",
        "nl2br",
        "sane_lists",
        "smarty",
    ]
    try:
        return md_lib.markdown(text, extensions=extensions)
    except Exception:
        return md_lib.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def generate_pdf(doc_path: Path, project_name: str, output_dir: Path) -> Path | None:
    doc_key = doc_path.stem
    meta = DOCUMENT_META.get(doc_key, {
        "title": doc_key.replace("-", " ").title(),
        "subtitle": "Document",
        "accent": "#333333",
        "icon": "📄",
    })

    text = doc_path.read_text(encoding="utf-8")
    body_html = md_to_html(text)

    css = CSS_TEMPLATE.format(
        accent=meta["accent"],
        project_name=project_name,
        doc_title=meta["title"],
    )

    html = HTML_TEMPLATE.format(
        css=css,
        doc_title=meta["title"],
        doc_subtitle=meta["subtitle"],
        project_name=project_name,
        date=datetime.now().strftime("%d %B %Y"),
        version="1.0",
        doc_id=doc_key.upper(),
        body=body_html,
    )

    output_path = output_dir / f"{doc_key}.pdf"

    if not WEASYPRINT_OK:
        # Fallback: salva HTML per ispezione
        html_path = output_dir / f"{doc_key}.html"
        html_path.write_text(html, encoding="utf-8")
        print(f"  ⚠ WeasyPrint non disponibile — salvato HTML: {html_path.name}")
        return html_path

    font_config = FontConfiguration()
    WeasyprintHTML(string=html).write_pdf(
        str(output_path),
        font_config=font_config,
    )
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AISA — Genera PDF professionali dai documenti del progetto",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("project", help="percorso del workspace di progetto (es. projects/mio-progetto)")
    parser.add_argument("--output", "-o", help="cartella di output (default: <project>/documents/)")
    args = parser.parse_args()

    project = Path(args.project)
    if not project.exists():
        print(f"ERRORE: workspace non trovato: {project}", file=sys.stderr)
        sys.exit(1)

    docs_dir = project / "documents"
    if not docs_dir.exists():
        print(f"ERRORE: cartella documents/ non trovata in {project}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output) if args.output else docs_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    project_name = project.name.replace("-", " ").title()

    order = ["requirements", "architecture", "implementation-plan"]
    docs = {p.stem: p for p in docs_dir.glob("*.md")}
    to_process = [docs[k] for k in order if k in docs] + [
        v for k, v in docs.items() if k not in order
    ]

    if not to_process:
        print(f"Nessun documento .md trovato in {docs_dir}")
        sys.exit(0)

    print(f"\nGenerazione PDF — {project_name}")
    print(f"{'─'*50}")

    generated = []
    for doc_path in to_process:
        print(f"  {doc_path.name}...", end="", flush=True)
        try:
            out = generate_pdf(doc_path, project_name, output_dir)
            size = out.stat().st_size
            print(f" ✓  ({size/1024:.0f} KB)")
            generated.append(out)
        except Exception as e:
            print(f" ✗  ERRORE: {e}")

    print(f"{'─'*50}")
    print(f"  {len(generated)} documenti generati in: {output_dir}/\n")


if __name__ == "__main__":
    main()
