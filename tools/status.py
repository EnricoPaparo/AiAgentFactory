#!/usr/bin/env python3
"""
Mostra lo stato operativo di un progetto AgentFactory.

Legge il Project Workspace e riporta:
- Human Gate Pending (bloccanti — richiedono azione immediata)
- Handoff prodotti con mittente e destinatario
- Deliverable presenti
- Knowledge Candidate e loro stato

Uso:
  python tools/status.py <project-id>
  python tools/status.py --all

Esempi:
  python tools/status.py my-api-project
  python tools/status.py --all
"""

import sys
import re
import argparse
from pathlib import Path

PROJECTS_DIR = Path("projects")


def extract_field(content, field):
    """Estrae il valore di un campo inline (- field: valore)."""
    pattern = rf"[-*]\s+{re.escape(field)}:\s*(.+)"
    m = re.search(pattern, content, re.IGNORECASE)
    return m.group(1).strip() if m else None


def extract_section(content, heading):
    """Estrae il testo della prima sezione con questo heading."""
    pattern = rf"^#{{2,}}\s+{re.escape(heading)}\s*$"
    lines = content.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.IGNORECASE):
            start = i + 1
            break
    if start is None:
        return None
    result = []
    for line in lines[start:]:
        if re.match(r"^#{2,}\s+", line):
            break
        result.append(line)
    return "\n".join(result).strip() or None


def human_gates(project_dir):
    gates_dir = project_dir / "human-gates"
    if not gates_dir.exists():
        return [], []
    pending, others = [], []
    for f in sorted(gates_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        status = (extract_field(content, "status") or "").strip("`").lower()
        gate_id = extract_field(content, "gate-id") or f.stem
        owner = extract_field(content, "decision-owner") or "—"
        scope = extract_section(content, "Blocking Scope") or "non specificato"
        scope_short = (scope[:72] + "...") if len(scope) > 72 else scope
        entry = {"id": gate_id, "file": f, "owner": owner, "scope": scope_short, "status": status}
        if status == "pending":
            pending.append(entry)
        else:
            others.append(entry)
    return pending, others


def handoffs(project_dir):
    d = project_dir / "handoffs"
    if not d.exists():
        return []
    result = []
    for f in sorted(d.glob("*.md")):
        if f.name.lower() == "readme.md":
            continue
        content = f.read_text(encoding="utf-8")
        result.append({
            "name": f.stem,
            "sender": extract_field(content, "sender") or "?",
            "recipient": extract_field(content, "recipient") or "?",
        })
    return result


def deliverables(project_dir):
    d = project_dir / "deliverables"
    return sorted(
        f.name for f in d.glob("*.md")
        if f.name.lower() != "readme.md"
    ) if d.exists() else []


def knowledge_candidates(project_dir):
    d = project_dir / "knowledge-candidates"
    if not d.exists():
        return []
    result = []
    for f in sorted(d.glob("*.md")):
        if f.name.lower() == "readme.md":
            continue
        content = f.read_text(encoding="utf-8")
        result.append({
            "name": f.stem,
            "status": extract_field(content, "status") or "?",
        })
    return result


def print_status(project_id):
    project_dir = PROJECTS_DIR / project_id

    if not project_dir.exists():
        print(f"ERRORE: progetto '{project_id}' non trovato in {PROJECTS_DIR}/")
        return False

    print(f"\n{'━'*60}")
    print(f"  {project_id}")
    print(f"{'━'*60}")

    # project-status.md overview
    status_file = project_dir / "project-status.md"
    if status_file.exists():
        content = status_file.read_text(encoding="utf-8")
        stato = extract_section(content, "Stato corrente") or "—"
        fase = extract_section(content, "Fase corrente") or "—"
        aggiornato = extract_section(content, "Ultimo aggiornamento") or "—"
        print(f"\n  Stato    : {stato}")
        print(f"  Fase     : {fase}")
        print(f"  Aggiorn. : {aggiornato}")

    # Human Gates
    pending, others = human_gates(project_dir)
    if pending:
        print(f"\n  ⚠  HUMAN GATE PENDING ({len(pending)}) — WORKFLOW BLOCCATO")
        for g in pending:
            print(f"\n     Gate   : {g['id']}")
            print(f"     Owner  : {g['owner']}")
            print(f"     Blocca : {g['scope']}")
            print(f"     File   : {g['file']}")
    else:
        closed = f" ({len(others)} chiusi)" if others else ""
        print(f"\n  ✓  Nessun Human Gate Pending{closed}")

    # Handoffs
    hoffs = handoffs(project_dir)
    if hoffs:
        print(f"\n  Handoff ({len(hoffs)}):")
        for h in hoffs:
            print(f"     {h['sender']} → {h['recipient']}   [{h['name']}]")
    else:
        print(f"\n  Handoff: nessuno")

    # Deliverables
    dels = deliverables(project_dir)
    if dels:
        print(f"\n  Deliverable ({len(dels)}):")
        for d in dels:
            print(f"     • {d}")
    else:
        print(f"\n  Deliverable: nessuno")

    # Knowledge Candidates
    kcs = knowledge_candidates(project_dir)
    if kcs:
        print(f"\n  Knowledge Candidate ({len(kcs)}):")
        for kc in kcs:
            print(f"     • {kc['name']}   [{kc['status']}]")

    print()
    return True


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("project_id", nargs="?", help="ID del progetto")
    group.add_argument("--all", "-a", action="store_true", help="Mostra tutti i progetti")
    args = parser.parse_args()

    if args.all:
        projects = sorted(
            p for p in PROJECTS_DIR.iterdir()
            if p.is_dir() and not p.name.startswith("_")
        )
        if not projects:
            print("Nessun progetto trovato.")
            sys.exit(0)
        ok = True
        for p in projects:
            ok = print_status(p.name) and ok
        sys.exit(0 if ok else 1)
    else:
        sys.exit(0 if print_status(args.project_id) else 1)


if __name__ == "__main__":
    main()
