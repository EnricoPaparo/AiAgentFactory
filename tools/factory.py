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
