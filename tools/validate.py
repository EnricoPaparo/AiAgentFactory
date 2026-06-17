#!/usr/bin/env python3
"""
AgentFactory artifact validator.

Valida artefatti di progetto (Agent Package, Handoff, Human Gate, Blueprint,
Capability, Knowledge Candidate) contro gli standard definiti in standards/.

Il validator e completamente data-driven: legge il frontmatter YAML di ogni
standard per sapere quale glob pattern usare e quali sezioni sono obbligatorie.
Nessun campo e hardcoded nel codice — aggiungere o rimuovere un campo obbligatorio
richiede solo modificare il frontmatter dello standard corrispondente.

Uso:
  python tools/validate.py <file1> [file2 ...]   # valida file specifici
  python tools/validate.py --full-check           # valida tutti gli artefatti del repo
  python tools/validate.py --list-standards       # mostra gli standard caricati

Esempi:
  python tools/validate.py projects/my-project/handoffs/dev-to-reviewer.md
  python tools/validate.py projects/my-project/generated-agents/developer.md
  python tools/validate.py --full-check
"""

import sys
import fnmatch
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERRORE: PyYAML richiesto. Installare con: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

STANDARDS_DIR = Path("standards")
REPO_ROOT = Path(".")


def load_standards(standards_dir=STANDARDS_DIR):
    """
    Carica tutti gli standard con frontmatter YAML da standards/.
    Ignora silenziosamente i file senza frontmatter (non tutti i file in
    standards/ devono essere uno standard con schema machine-readable).
    """
    registry = []
    for std_file in sorted(standards_dir.glob("*-standard.md")):
        content = std_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        try:
            end = content.index("---", 3)
            meta = yaml.safe_load(content[3:end])
        except (ValueError, yaml.YAMLError) as e:
            print(f"WARN: frontmatter non valido in {std_file}: {e}", file=sys.stderr)
            continue
        if not isinstance(meta, dict) or "applies-to" not in meta:
            continue
        meta["_source_file"] = str(std_file)
        registry.append(meta)
    return registry


def find_standard(artifact_path, registry):
    """
    Trova il primo standard il cui glob pattern (applies-to) corrisponde
    al percorso dell'artefatto. Usa fnmatch per compatibilita massima.
    Restituisce None se nessuno standard e applicabile.
    """
    rel = str(Path(artifact_path)).replace("\\", "/")
    for std in registry:
        pattern = std["applies-to"].replace("\\", "/")
        if fnmatch.fnmatch(rel, pattern):
            return std
    return None


def validate_file(artifact_path, registry):
    """
    Valida un singolo artefatto contro il suo standard.

    Restituisce:
      (standard_name: str, errors: list[str])
      Se nessuno standard e applicabile, restituisce (None, []).
    """
    std = find_standard(artifact_path, registry)
    if std is None:
        return None, []

    try:
        content = Path(artifact_path).read_text(encoding="utf-8")
    except (OSError, IOError) as e:
        return std.get("standard", "?"), [f"impossibile leggere il file: {e}"]

    lines = set(line.rstrip() for line in content.splitlines())
    errors = []
    for section in std.get("required-sections", []):
        if section not in lines:
            errors.append(f"sezione mancante: {section}")

    return std.get("standard", "?"), errors


def find_all_artifacts(registry, repo_root=REPO_ROOT):
    """
    Trova tutti i file nel repo che corrispondono al pattern applies-to
    di almeno uno standard. Usa pathlib.glob per correttezza path-aware.
    """
    artifacts = set()
    for std in registry:
        pattern = std["applies-to"]
        for path in repo_root.glob(pattern):
            if path.is_file():
                artifacts.add(path)
    return sorted(artifacts)


def print_standards(registry):
    """Stampa un riepilogo degli standard caricati."""
    if not registry:
        print("Nessuno standard con frontmatter trovato.")
        return
    print(f"Standard caricati ({len(registry)}):\n")
    for std in registry:
        name = std.get("standard", "?")
        pattern = std.get("applies-to", "?")
        required = std.get("required-sections", [])
        optional = std.get("optional-sections", [])
        source = std.get("_source_file", "?")
        print(f"  {name}")
        print(f"    pattern : {pattern}")
        print(f"    required: {len(required)} sezioni")
        print(f"    optional: {len(optional)} sezioni")
        print(f"    standard: {source}")
        print()


def main():
    args = sys.argv[1:]

    if not args or "-h" in args or "--help" in args:
        print(__doc__)
        sys.exit(0)

    registry = load_standards()
    if not registry:
        print("WARN: nessuno standard con frontmatter trovato in standards/")
        sys.exit(0)

    if "--list-standards" in args:
        print_standards(registry)
        sys.exit(0)

    full_check = "--full-check" in args
    file_args = [a for a in args if not a.startswith("--")]

    if full_check:
        files_to_check = find_all_artifacts(registry)
        if not files_to_check:
            print("Nessun artefatto trovato nel repo che corrisponda a uno standard.")
            sys.exit(0)
    else:
        if not file_args:
            print(__doc__)
            sys.exit(0)
        files_to_check = [Path(a) for a in file_args]

    exit_code = 0
    checked = 0
    skipped = 0
    failed = 0

    for artifact in files_to_check:
        if not Path(artifact).exists():
            print(f"SKIP [{artifact}] → file non trovato")
            skipped += 1
            continue

        standard_name, errors = validate_file(artifact, registry)

        if standard_name is None:
            skipped += 1
            continue

        checked += 1
        if errors:
            failed += 1
            print(f"FAIL [{artifact}]  (standard: {standard_name})")
            for e in errors:
                print(f"     ✗ {e}")
            exit_code = 1
        else:
            print(f"OK   [{artifact}]  (standard: {standard_name})")

    print(f"\nRisultato: {checked} validati, {failed} falliti, {skipped} saltati.")
    if exit_code != 0:
        print("Validazione fallita — correggere le sezioni mancanti prima del merge.")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
