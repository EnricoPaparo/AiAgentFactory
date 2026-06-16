#!/usr/bin/env python3
"""Minimal deterministic AgentFactory runner utilities.

This tool does not call AI backends. It handles operational plumbing that should
not consume model tokens: state inspection, validation, packet display and human
gate approval bookkeeping.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ALLOWED_PHASES = {
    "intake",
    "requirements",
    "requirements_approval",
    "solution",
    "solution_approval",
    "execution_plan",
    "execution_plan_approval",
    "agent_generation",
    "execution",
    "review",
    "supervision",
    "final_delivery_approval",
    "closed",
}

ALLOWED_STATUS = {"active", "blocked", "waiting_for_human", "completed", "failed"}

STATE_REQUIRED = {
    "project_id",
    "phase",
    "status",
    "pending_gate",
    "next_action",
    "artifact_index",
    "approved_summaries",
    "runtime_packets",
    "run_records",
    "updated_at",
}

PACKET_REQUIRED = {
    "packet_id",
    "project_id",
    "agent_package",
    "agent_role",
    "context_budget",
    "task",
    "approved_context",
    "required_files",
    "must_not",
    "expected_outputs",
    "handoff_required",
    "gate_status",
}

APPROVAL_PHASE_MAP = {
    "approve-requirements": ("solution", "run_architect"),
    "approve-solution-blueprint": ("execution_plan", "run_pipeline_designer"),
    "approve-execution-plan": ("agent_generation", "run_knowledge_compiler"),
    "approve-final-delivery": ("closed", "none"),
}

PROJECT_DIRS = [
    "input",
    "blueprints",
    "summaries",
    "generated-agents",
    "runtime-packets",
    "handoffs",
    "human-gates",
    "deliverables",
    "reviews",
    "run-records",
    "knowledge-candidates",
]


def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def project_path(value: str) -> Path:
    path = Path(value)
    if not path.exists():
        die(f"project path does not exist: {path}")
    if not path.is_dir():
        die(f"project path is not a directory: {path}")
    return path


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"missing JSON file: {path}")
    except json.JSONDecodeError as exc:
        die(f"invalid JSON in {path}: {exc}")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def kebab_case(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug or "agentfactory-project"


def infer_project_id(idea: str) -> str:
    quoted = re.findall(r'"([^"]+)"', idea)
    if quoted:
        return kebab_case(quoted[0])[:64].strip("-")
    words = re.findall(r"[A-Za-zÀ-ÿ0-9]+", idea)
    stop = {
        "voglio",
        "creare",
        "un",
        "una",
        "per",
        "con",
        "che",
        "deve",
        "fare",
        "sito",
        "web",
        "landing",
        "page",
        "app",
        "progetto",
    }
    selected = [word for word in words if word.lower() not in stop][:5]
    return kebab_case(" ".join(selected))[:64].strip("-") or "agentfactory-project"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_state(project: Path) -> dict[str, Any]:
    return load_json(project / "factory-state.json")


def gate_path(project: Path, gate_id: str) -> Path:
    path = project / "human-gates" / f"{gate_id}.md"
    if not path.exists():
        die(f"missing gate file: {path}")
    return path


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^({re.escape(prefix)}).*?$", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(replacement, text)
    return text + f"\n{replacement}\n"


def gate_status(text: str) -> str | None:
    match = re.search(r"^- status:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def create_run_record(
    project: Path,
    action: str,
    status: str,
    inputs: list[str],
    outputs: list[str],
    checks: list[str],
    token_notes: str,
    residual_risks: str = "None.",
) -> Path:
    records = project / "run-records"
    records.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    record_id = f"{timestamp}-{action}"
    project_id = project.name
    body = [
        f"# Run Record: {record_id}",
        "",
        "## Metadata",
        "",
        f"- record-id: {record_id}",
        f"- project-id: {project_id}",
        f"- created-at: {datetime.now().isoformat(timespec='seconds')}",
        "- actor: tools/factory.py",
        f"- action: {action}",
        f"- status: {status}",
        "",
        "## Inputs",
        "",
        *[f"- {item}" for item in inputs],
        "",
        "## Outputs",
        "",
        *[f"- {item}" for item in outputs],
        "",
        "## Checks",
        "",
        *[f"- {item}" for item in checks],
        "",
        "## Token Notes",
        "",
        token_notes,
        "",
        "## Residual Risks",
        "",
        residual_risks,
        "",
    ]
    path = records / f"{record_id}.md"
    path.write_text("\n".join(body), encoding="utf-8")
    return path


def bootstrap_readme(project_id: str) -> str:
    return f"""# Project Workspace: {project_id}

## Purpose

Workspace AgentFactory creato da `tools/factory.py start`.

## Current Phase

Requirements.

## Primary Artifacts

- `input/initial-request.md`
- `factory-state.json`
- `artifact-index.md`
- `project-status.md`
- `blueprints/bootstrap-execution-blueprint.md`
- `generated-agents/requirement-analyst-agent-package.md`
- `human-gates/approve-requirements.md`
"""


def bootstrap_status(project_id: str, today: str) -> str:
    return f"""# Project Status: {project_id}

## Metadata

- project-id: {project_id}
- status: active
- current-phase: requirements
- current-agent: Requirement Analyst
- factory-state: factory-state.json
- artifact-index: artifact-index.md
- created-at: {today}
- updated-at: {today}
- owner: Human Maintainer

## Phase Checklist

| Phase | Status | Main Artifact | Notes |
|---|---|---|---|
| Intake | Completed | `input/initial-request.md` | Initial request captured. |
| Requirements | Pending | `blueprints/requirements-blueprint.md` | Next action. |
| Solution | Pending | `blueprints/solution-blueprint.md` | Blocked by `approve-requirements`. |
| Execution Plan | Pending | `blueprints/execution-blueprint.md` | Not started. |
| Agent Generation | Pending | `generated-agents/` | Not started. |
| Execution | Pending | `deliverables/`, `handoffs/` | Not started. |
| Review | Pending | `reviews/` | Not started. |
| Run Records | Active | `run-records/` | Bootstrap record created. |
| Knowledge Evolution | Pending | `knowledge-candidates/` | Not started. |
| Closure | Pending | final handoff | Not started. |

## Active Human Gates

| Gate | Status | Blocking Scope | Decision Owner |
|---|---|---|---|
| approve-requirements | Pending | solution blueprint generation | Human Maintainer |
| approve-solution-blueprint | Expected | execution blueprint generation | Human Maintainer |
| approve-execution-plan | Expected | agent package generation and project execution | Human Maintainer |
| approve-final-delivery | Expected | project closure | Human Maintainer |

## Next Action

Run Requirement Analyst and produce `blueprints/requirements-blueprint.md`.
"""


def bootstrap_blueprint(project_id: str, today: str) -> str:
    return f"""# Bootstrap Execution Blueprint: {project_id}

## Metadata

- project-id: {project_id}
- created-by: Factory Intake
- created-at: {today}
- runtime-adapter: runtime-adapters/codex-conversation.md
- runner: tools/factory.py start

## Scope

Create the minimum Project Workspace and prepare Requirement Analyst execution only.

## Source Request

- projects/{project_id}/input/initial-request.md

## Created Bootstrap Artifacts

- projects/{project_id}/README.md
- projects/{project_id}/project-status.md
- projects/{project_id}/factory-state.json
- projects/{project_id}/artifact-index.md
- projects/{project_id}/input/initial-request.md
- projects/{project_id}/blueprints/bootstrap-execution-blueprint.md
- projects/{project_id}/generated-agents/requirement-analyst-agent-package.md
- projects/{project_id}/human-gates/approve-requirements.md

## First Agent

- agent-role: Requirement Analyst
- permanent-agent-source: agents/requirement-analyst/requirement-analyst.md
- expected-output: projects/{project_id}/blueprints/requirements-blueprint.md

## Human Gates

- approve-requirements: created as Pending; blocks `solution blueprint generation`, not Requirement Analyst.

## Out Of Scope

- Requirements Blueprint content.
- Architecture decisions.
- Stack decisions.
- Temporary operational agent generation.
- Deliverable implementation.

## Next Runtime Action

Run Requirement Analyst in Codex or a future backend, then stop at `approve-requirements`.
"""


def requirement_package(project_id: str) -> str:
    return f"""# Agent Package: requirement-analyst-{project_id}

## Metadata

- project-id: {project_id}
- package-id: requirement-analyst-{project_id}
- agent-role: Requirement Analyst
- agent-source: permanent agent `agents/requirement-analyst/requirement-analyst.md`
- runtime-adapter: runtime-adapters/codex-conversation.md

## Task

Transform the initial request into a verifiable Requirements Blueprint for this project.

## Inputs

- projects/{project_id}/input/initial-request.md
- agents/requirement-analyst/requirement-analyst.md
- standards/requirements-blueprint-standard.md
- standards/handoff-standard.md

## Expected Outputs

- projects/{project_id}/blueprints/requirements-blueprint.md
- projects/{project_id}/handoffs/requirement-analyst-to-architect.md

## Boundaries

- Do not choose architecture or technology stack.
- Do not implement deliverables.
- Preserve explicit user constraints.
- Separate assumptions from requirements.

## Workflow

1. Read the initial request.
2. Extract goal, output, requirements, constraints, assumptions, ambiguities and out-of-scope items.
3. Write acceptance criteria suitable for final review.
4. Produce handoff to Architect.
5. Stop at `approve-requirements`.

## Definition Of Done

- Requirements Blueprint follows `standards/requirements-blueprint-standard.md`.
- Functional requirements are verifiable.
- Handoff to Architect is present.
- No architecture or stack decision is made.
"""


def approve_requirements_gate(project_id: str, today: str) -> str:
    return f"""# Human Gate: approve-requirements

## Metadata

- gate-id: approve-requirements
- project-id: {project_id}
- status: Pending
- requested-by: Requirement Analyst
- decision-owner: Human Maintainer
- created-at: {today}
- decided-at:
- expires-at:

## Decision Required

Approve the Requirements Blueprint before Architect generates the Solution Blueprint.

## Context

- Initial request: projects/{project_id}/input/initial-request.md
- Future Requirements Blueprint: projects/{project_id}/blueprints/requirements-blueprint.md
- Bootstrap blueprint: projects/{project_id}/blueprints/bootstrap-execution-blueprint.md

## Options

- Approved
- Changes Requested
- Rejected

## Approval Criteria

- Requirements preserve the original user intent.
- Constraints are explicit and verifiable.
- Ambiguities and assumptions are separated.
- No architecture, stack or implementation decision is included.

## Impact If Approved

Architect may generate the Solution Blueprint.

## Impact If Rejected

The project remains blocked and must not proceed to architecture.

## Return To Phase

Requirement Analyst.

## Blocking Scope

Solution blueprint generation.

## Human Decision

- decision:
- decided-by:
- decided-at:
- notes:
"""


def artifact_index(project_id: str) -> str:
    return f"""# Artifact Index: {project_id}

## Core Artifacts

| Artifact | Path | Status | Notes |
|---|---|---|---|
| Initial request | `input/initial-request.md` | Completed | Preserved user idea. |
| Factory state | `factory-state.json` | Active | Next action is Requirement Analyst. |
| Project status | `project-status.md` | Active | Human-readable status. |
| Bootstrap blueprint | `blueprints/bootstrap-execution-blueprint.md` | Completed | Created by Factory start. |
| Requirement Analyst package | `generated-agents/requirement-analyst-agent-package.md` | Ready | First agent package. |
| approve-requirements gate | `human-gates/approve-requirements.md` | Pending | Blocks solution generation. |

## Approved Summaries

| Summary | Source | Gate | Status |
|---|---|---|---|

## Runtime Packets

| Packet | Agent package | Status |
|---|---|---|

## Run Records

| Record | Action | Status |
|---|---|---|
| `run-records/` | bootstrap-start | completed |
"""


def requirement_prompt(project_id: str) -> str:
    return f"""Esegui il Requirement Analyst per questo progetto AgentFactory.

Repository:
<repository-path>

Project Workspace:
projects/{project_id}

Agent Package:
projects/{project_id}/generated-agents/requirement-analyst-agent-package.md

Regole:
- Leggi l'Agent Package e gli input indicati.
- Produci `projects/{project_id}/blueprints/requirements-blueprint.md`.
- Produci `projects/{project_id}/handoffs/requirement-analyst-to-architect.md`.
- Non scegliere architettura, stack o piano operativo.
- Non implementare deliverable.
- Quando hai finito, fermati su `human-gates/approve-requirements.md` e chiedi approval.
- Aggiorna `factory-state.json` a phase `requirements_approval`, status `waiting_for_human`, pending_gate `approve-requirements`, next_action `wait_for_human_approval`.
"""


def cmd_next(args: argparse.Namespace) -> None:
    project = project_path(args.project)
    state = read_state(project)
    print(f"project: {state.get('project_id')}")
    print(f"phase: {state.get('phase')}")
    print(f"status: {state.get('status')}")
    print(f"pending_gate: {state.get('pending_gate')}")
    print(f"next_action: {state.get('next_action')}")
    if state.get("pending_gate"):
        gate = gate_path(project, state["pending_gate"])
        text = gate.read_text(encoding="utf-8")
        print(f"gate_file: {gate}")
        print(f"gate_status: {gate_status(text)}")


def cmd_start(args: argparse.Namespace) -> None:
    idea = args.idea.strip()
    if not idea:
        die("idea cannot be empty")

    repo = Path.cwd()
    projects_dir = repo / "projects"
    projects_dir.mkdir(exist_ok=True)
    project_id = kebab_case(args.project_id) if args.project_id else infer_project_id(idea)
    project = projects_dir / project_id
    if project.exists() and not args.force:
        die(f"project already exists: {project}. Use --force only if you intentionally want to reuse it.")

    project.mkdir(exist_ok=True)
    for name in PROJECT_DIRS:
        (project / name).mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    write_text(project / "README.md", bootstrap_readme(project_id))
    write_text(project / "input" / "initial-request.md", f"# Initial Request: {project_id}\n\n{idea}")
    write_text(project / "project-status.md", bootstrap_status(project_id, today))
    write_text(project / "artifact-index.md", artifact_index(project_id))
    write_text(project / "blueprints" / "bootstrap-execution-blueprint.md", bootstrap_blueprint(project_id, today))
    write_text(project / "generated-agents" / "requirement-analyst-agent-package.md", requirement_package(project_id))
    write_text(project / "human-gates" / "approve-requirements.md", approve_requirements_gate(project_id, today))

    state = {
        "project_id": project_id,
        "phase": "requirements",
        "status": "active",
        "pending_gate": None,
        "next_action": "run_requirement_analyst",
        "artifact_index": "artifact-index.md",
        "approved_summaries": [],
        "runtime_packets": [],
        "run_records": "run-records/",
        "updated_at": today,
    }
    write_json(project / "factory-state.json", state)

    record = create_run_record(
        project=project,
        action="start",
        status="completed",
        inputs=["user idea"],
        outputs=[
            "README.md",
            "input/initial-request.md",
            "project-status.md",
            "factory-state.json",
            "artifact-index.md",
            "blueprints/bootstrap-execution-blueprint.md",
            "generated-agents/requirement-analyst-agent-package.md",
            "human-gates/approve-requirements.md",
        ],
        checks=["Project workspace created.", "Requirement Analyst package created.", "approve-requirements gate created."],
        token_notes="Bootstrap handled deterministically by CLI; no model context required.",
    )

    prompt_path = project / "run-records" / "next-requirement-analyst-prompt.md"
    write_text(prompt_path, requirement_prompt(project_id).replace("<repository-path>", str(repo)))

    print(f"project_id: {project_id}")
    print(f"workspace: {project}")
    print("next_action: run_requirement_analyst")
    print(f"run_record: {record}")
    print(f"next_prompt: {prompt_path}")


def cmd_packet(args: argparse.Namespace) -> None:
    project = project_path(args.project)
    packet = project / "runtime-packets" / f"{args.packet}.json"
    data = load_json(packet)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def validate_project(project: Path) -> list[str]:
    errors: list[str] = []
    state_path = project / "factory-state.json"
    if not state_path.exists():
        errors.append("missing factory-state.json")
        return errors

    state = load_json(state_path)
    missing = sorted(STATE_REQUIRED - set(state))
    if missing:
        errors.append(f"factory-state missing keys: {', '.join(missing)}")
    if state.get("phase") not in ALLOWED_PHASES:
        errors.append(f"invalid phase: {state.get('phase')}")
    if state.get("status") not in ALLOWED_STATUS:
        errors.append(f"invalid status: {state.get('status')}")
    if state.get("status") != "waiting_for_human" and state.get("pending_gate") is not None:
        errors.append("pending_gate must be null unless status is waiting_for_human")

    artifact_index = state.get("artifact_index")
    if artifact_index and not (project / artifact_index).exists():
        errors.append(f"artifact_index not found: {artifact_index}")

    for summary in state.get("approved_summaries", []):
        if not (project / summary).exists():
            errors.append(f"approved summary not found: {summary}")

    for packet_ref in state.get("runtime_packets", []):
        packet_path = project / packet_ref
        if not packet_path.exists():
            errors.append(f"runtime packet not found: {packet_ref}")
            continue
        packet = load_json(packet_path)
        missing_packet = sorted(PACKET_REQUIRED - set(packet))
        if missing_packet:
            errors.append(f"{packet_ref} missing keys: {', '.join(missing_packet)}")
        agent_package = packet.get("agent_package")
        if agent_package and not (project / agent_package).exists():
            errors.append(f"{packet_ref} agent_package not found: {agent_package}")
        for required in packet.get("required_files", []):
            candidate = project / required
            if not candidate.exists():
                # Allow repository-root relative references for standards/capabilities.
                repo_candidate = project.parents[1] / required if len(project.parents) > 1 else candidate
                if not repo_candidate.exists():
                    errors.append(f"{packet_ref} required file not found: {required}")

    pending_gate = state.get("pending_gate")
    if pending_gate:
        path = project / "human-gates" / f"{pending_gate}.md"
        if not path.exists():
            errors.append(f"pending gate file not found: {pending_gate}")

    run_records = state.get("run_records")
    if run_records and not (project / run_records).exists():
        errors.append(f"run_records path not found: {run_records}")

    return errors


def cmd_validate(args: argparse.Namespace) -> None:
    project = project_path(args.project)
    errors = validate_project(project)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    print("validation: pass")


def cmd_approve(args: argparse.Namespace) -> None:
    project = project_path(args.project)
    decision = args.decision
    if decision not in {"Approved", "Changes Requested", "Rejected"}:
        die("decision must be Approved, Changes Requested or Rejected")

    state = read_state(project)
    gate = gate_path(project, args.gate)
    text = gate.read_text(encoding="utf-8")
    previous = gate_status(text) or "Unknown"
    now = datetime.now().strftime("%Y-%m-%d")

    text = replace_line(text, "- status:", f"- status: {decision}")
    text = replace_line(text, "- decided-at:", f"- decided-at: {now}")
    text = replace_line(text, "- decision:", f"- decision: {decision}")
    text = replace_line(text, "- decided-by:", f"- decided-by: {args.decided_by}")
    text = replace_line(text, "- notes:", f"- notes: {args.notes}")
    gate.write_text(text, encoding="utf-8")

    if decision == "Approved":
        phase, next_action = APPROVAL_PHASE_MAP.get(args.gate, (state.get("phase", "blocked"), "determine_next_action"))
        state["phase"] = phase
        state["status"] = "completed" if phase == "closed" else "active"
        state["pending_gate"] = None
        state["next_action"] = next_action
    else:
        state["status"] = "blocked"
        state["pending_gate"] = None
        state["next_action"] = "route_changes_or_stop"
    state["updated_at"] = now
    write_json(project / "factory-state.json", state)

    record = create_run_record(
        project=project,
        action=f"approve-{args.gate}",
        status="completed" if decision == "Approved" else "changes-requested",
        inputs=[str(gate.relative_to(project)), "factory-state.json"],
        outputs=[str(gate.relative_to(project)), "factory-state.json"],
        checks=[f"Gate status changed from {previous} to {decision}.", "Factory state updated."],
        token_notes="Approval handled deterministically by CLI; no model context required.",
        residual_risks="Downstream artifacts may need regeneration if decision is not Approved.",
    )
    print(f"gate: {args.gate}")
    print(f"decision: {decision}")
    print(f"state_phase: {state['phase']}")
    print(f"state_status: {state['status']}")
    print(f"run_record: {record}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="factory", description="Minimal AgentFactory operational runner")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="bootstrap a new project workspace from an idea")
    p_start.add_argument("idea")
    p_start.add_argument("--project-id")
    p_start.add_argument("--force", action="store_true")
    p_start.set_defaults(func=cmd_start)

    p_next = sub.add_parser("next", help="show current phase, pending gate and next action")
    p_next.add_argument("project")
    p_next.set_defaults(func=cmd_next)

    p_validate = sub.add_parser("validate", help="validate state, summaries and runtime packets")
    p_validate.add_argument("project")
    p_validate.set_defaults(func=cmd_validate)

    p_packet = sub.add_parser("packet", help="print one runtime packet")
    p_packet.add_argument("project")
    p_packet.add_argument("packet")
    p_packet.set_defaults(func=cmd_packet)

    p_approve = sub.add_parser("approve", help="record a human gate decision")
    p_approve.add_argument("project")
    p_approve.add_argument("gate")
    p_approve.add_argument("--decision", required=True)
    p_approve.add_argument("--decided-by", default="Human Maintainer")
    p_approve.add_argument("--notes", default="Approved through Factory Runner CLI.")
    p_approve.set_defaults(func=cmd_approve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
