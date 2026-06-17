#!/usr/bin/env python3
"""
Crea un nuovo Project Workspace copiando projects/_template/.

Uso:
  python tools/new-project.py <project-id>
  python tools/new-project.py <project-id> --request "Descrizione del progetto"

Esempi:
  python tools/new-project.py my-api-project
  python tools/new-project.py my-api-project --request "API REST per gestione utenti"
"""

import sys
import shutil
import argparse
from pathlib import Path
from datetime import date

TEMPLATE_DIR = Path("projects/_template")
PROJECTS_DIR = Path("projects")


def create_project(project_id, initial_request=None):
    dest = PROJECTS_DIR / project_id

    if dest.exists():
        print(f"ERRORE: il progetto '{project_id}' esiste già in {dest}")
        sys.exit(1)

    if not TEMPLATE_DIR.exists():
        print(f"ERRORE: template non trovato in {TEMPLATE_DIR}")
        sys.exit(1)

    shutil.copytree(TEMPLATE_DIR, dest)

    (dest / "project-status.md").write_text(
        f"# Project Status: {project_id}\n\n"
        f"## Stato corrente\n\nIn corso\n\n"
        f"## Fase corrente\n\nInput — in attesa di Requirements Blueprint\n\n"
        f"## Human Gate aperti\n\nNessuno\n\n"
        f"## Agenti attivi\n\nNessuno\n\n"
        f"## Deliverable prodotti\n\nNessuno\n\n"
        f"## Knowledge Candidate\n\nNessuna\n\n"
        f"## Ultimo aggiornamento\n\n{date.today()} — progetto creato\n",
        encoding="utf-8"
    )

    if initial_request:
        (dest / "input" / "initial-request.md").write_text(
            f"# Initial Request: {project_id}\n\n"
            f"## Data\n\n{date.today()}\n\n"
            f"## Richiesta\n\n{initial_request}\n\n"
            f"## Note\n\n"
            f"Completare con vincoli, contesto e materiali aggiuntivi se disponibili.\n",
            encoding="utf-8"
        )

    print(f"Progetto creato: {dest}/")
    print(f"\nProssimi passi:")
    print(f"  1. Completare {dest}/input/initial-request.md")
    print(f"  2. Aprire OpenCode nella radice del repo")
    print(f"  3. Seguire la guida in {dest}/README.md")
    if initial_request:
        print(f"\nRichiesta iniziale salvata in {dest}/input/initial-request.md")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="ID del progetto (kebab-case, es. my-api-project)")
    parser.add_argument("--request", "-r", metavar="TESTO",
                        help="Richiesta iniziale del progetto (opzionale)")
    args = parser.parse_args()

    project_id = args.project_id
    if not all(c.isalnum() or c in "-_" for c in project_id):
        print(f"ERRORE: project-id deve essere kebab-case (lettere, numeri, trattini)")
        sys.exit(1)

    if project_id.startswith("_"):
        print(f"ERRORE: i project-id che iniziano con '_' sono riservati ai template")
        sys.exit(1)

    create_project(project_id, args.request)


if __name__ == "__main__":
    main()
