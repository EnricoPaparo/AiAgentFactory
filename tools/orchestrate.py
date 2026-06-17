#!/usr/bin/env python3
"""
Orchestratore AgentFactory.

Legge workflow.yml dal project workspace ed esegue automaticamente la pipeline
di agenti AI: step sequenziali, step paralleli, Human Gate interattivi,
chiarimenti all'utente, validazione output e ripresa da uno step specifico.

Uso:
  python tools/orchestrate.py <project-id>
  python tools/orchestrate.py <project-id> --from <step-id>
  python tools/orchestrate.py <project-id> --dry-run
  python tools/orchestrate.py <project-id> --model claude-sonnet-4-6

Esempi:
  python tools/orchestrate.py my-api-project
  python tools/orchestrate.py my-api-project --from architect
  python tools/orchestrate.py my-api-project --dry-run
"""

import sys
import re
import json
import asyncio
import threading
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERRORE: PyYAML richiesto. Installa con: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    import anthropic
except ImportError:
    print("ERRORE: anthropic SDK richiesto. Installa con: pip install anthropic", file=sys.stderr)
    sys.exit(1)

PROJECTS_DIR = Path("projects")
REPO_ROOT = Path(".")
DEFAULT_MODEL = "claude-opus-4-8"
MAX_TOOL_CALLS = 40

TOOLS = [
    {
        "name": "read_file",
        "description": (
            "Leggi il contenuto di un file. Usa percorsi relativi alla radice del repository. "
            "Esempi: 'projects/my-project/input/initial-request.md', "
            "'standards/agent-package-standard.md', 'capabilities/git.md'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Percorso del file relativo alla radice del repository.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": (
            "Crea o sovrascrive un file nel project workspace. "
            "Usa percorsi relativi al project workspace "
            "(es. 'blueprints/requirements-blueprint.md', 'handoffs/dev-to-reviewer.md'). "
            "Le directory intermedie vengono create automaticamente."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Percorso relativo al project workspace.",
                },
                "content": {
                    "type": "string",
                    "description": "Contenuto completo del file.",
                },
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "list_files",
        "description": "Elenca file e directory in un percorso del repository.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Percorso relativo alla radice del repository. "
                        "Se omesso, elenca il project workspace."
                    ),
                }
            },
            "required": [],
        },
    },
    {
        "name": "request_clarification",
        "description": (
            "Poni domande all'utente umano quando hai dubbi critici non risolvibili "
            "con le informazioni disponibili. L'esecuzione si mette in pausa finché "
            "l'utente non risponde. Usa solo per dubbi bloccanti — non per conferme di routine."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista di domande da porre all'utente.",
                },
                "context": {
                    "type": "string",
                    "description": "Contesto che aiuta l'utente a capire perché queste domande sono necessarie.",
                },
            },
            "required": ["questions"],
        },
    },
    {
        "name": "complete_task",
        "description": (
            "Dichiara il completamento del task. Chiama SEMPRE questo tool al termine, "
            "sia in caso di successo che di blocco o fallimento. "
            "Non terminare la sessione senza averlo chiamato."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["completed", "blocked", "changes-requested", "failed"],
                    "description": (
                        "Stato finale: "
                        "completed=output prodotti e DoD verificata; "
                        "blocked=input mancante o Human Gate pendente; "
                        "changes-requested=review ha richiesto modifiche; "
                        "failed=task non completabile."
                    ),
                },
                "summary": {
                    "type": "string",
                    "description": (
                        "Riepilogo: cosa è stato fatto, file prodotti, "
                        "verifiche eseguite, rischi residui, prossimo agente suggerito."
                    ),
                },
                "files_created": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista dei file creati o modificati (percorsi relativi al project workspace).",
                },
            },
            "required": ["status", "summary"],
        },
    },
]


class Orchestrator:
    def __init__(self, project_id: str, model: str = DEFAULT_MODEL):
        self.project_id = project_id
        self.project_dir = PROJECTS_DIR / project_id
        self.model = model
        self.state_file = self.project_dir / ".orchestrator-state.json"
        self.state = self._load_state()
        self.client = anthropic.Anthropic()
        self._clarification_lock = threading.Lock()

    # ── State management ──────────────────────────────────────────────────────

    def _load_state(self) -> dict:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"completed": {}, "failed": []}

    def _save_state(self):
        self.state_file.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def reset_from(self, from_step: str):
        """Remove from_step and all later steps from completed state."""
        workflow = self.load_workflow()
        all_ids = self._collect_step_ids(workflow.get("steps", []))
        if from_step not in all_ids:
            print(f"ERRORE: step '{from_step}' non trovato nel workflow.", file=sys.stderr)
            sys.exit(1)
        removing = False
        for sid in all_ids:
            if sid == from_step:
                removing = True
            if removing:
                self.state["completed"].pop(sid, None)
                if sid in self.state["failed"]:
                    self.state["failed"].remove(sid)
        self._save_state()

    def _collect_step_ids(self, steps: list) -> list:
        ids = []
        for item in steps:
            if "parallel" in item:
                for s in item["parallel"]:
                    ids.append(s["id"])
            elif "id" in item:
                ids.append(item["id"])
        return ids

    # ── Workflow loading ───────────────────────────────────────────────────────

    def load_workflow(self) -> dict:
        wf_file = self.project_dir / "blueprints" / "workflow.yml"
        if not wf_file.exists():
            raise FileNotFoundError(
                f"workflow.yml non trovato: {wf_file}\n"
                "Crea il file seguendo il template in projects/_template/blueprints/workflow.yml"
            )
        return yaml.safe_load(wf_file.read_text(encoding="utf-8"))

    # ── Tool handlers ──────────────────────────────────────────────────────────

    def _tool_read_file(self, path: str) -> str:
        p = REPO_ROOT / path
        if not p.exists():
            return f"ERRORE: file non trovato: {path}"
        try:
            return p.read_text(encoding="utf-8")
        except Exception as e:
            return f"ERRORE lettura: {e}"

    def _tool_write_file(self, path: str, content: str) -> str:
        p = self.project_dir / path
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return f"Scritto: {p}"
        except Exception as e:
            return f"ERRORE scrittura: {e}"

    def _tool_list_files(self, path: str = None) -> str:
        target = REPO_ROOT / path if path else self.project_dir
        if not target.exists():
            return f"ERRORE: directory non trovata: {path}"
        try:
            lines = []
            for item in sorted(target.iterdir()):
                lines.append(f"{'  ' if item.is_dir() else '  '}{item.name}{'/' if item.is_dir() else ''}")
            return "\n".join(lines) if lines else "(directory vuota)"
        except Exception as e:
            return f"ERRORE: {e}"

    def _tool_request_clarification(self, questions: list, context: str = None) -> str:
        with self._clarification_lock:
            print(f"\n{'─'*60}")
            print("  CHIARIMENTO RICHIESTO DALL'AGENTE")
            if context:
                print(f"\n  Contesto: {context}")
            print(f"{'─'*60}")
            answers = {}
            for i, q in enumerate(questions, 1):
                print(f"\n  Domanda {i}: {q}")
                try:
                    answer = input("  Risposta: ").strip()
                except EOFError:
                    answer = ""
                answers[f"domanda_{i}"] = {"domanda": q, "risposta": answer}
            print(f"{'─'*60}\n")
            return json.dumps(answers, ensure_ascii=False, indent=2)

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "read_file":
            return self._tool_read_file(tool_input["path"])
        if tool_name == "write_file":
            return self._tool_write_file(tool_input["path"], tool_input["content"])
        if tool_name == "list_files":
            return self._tool_list_files(tool_input.get("path"))
        if tool_name == "request_clarification":
            return self._tool_request_clarification(
                tool_input["questions"], tool_input.get("context")
            )
        if tool_name == "complete_task":
            return json.dumps(tool_input, ensure_ascii=False)
        return f"ERRORE: tool sconosciuto: {tool_name}"

    # ── Agent execution ────────────────────────────────────────────────────────

    def _load_agent_content(self, step: dict) -> str:
        agent_path = step.get("agent") or step.get("package")
        if not agent_path:
            return f"# Task: {step.get('name', step['id'])}\n\nEsegui il task assegnato."
        for base in (REPO_ROOT, self.project_dir):
            p = base / agent_path
            if p.exists():
                return p.read_text(encoding="utf-8")
        return f"[AGENTE NON TROVATO: {agent_path}]\nEsegui il task assegnato con le informazioni disponibili."

    def _load_inputs(self, step: dict) -> dict:
        result = {}
        for inp in step.get("inputs", []):
            for base in (self.project_dir, REPO_ROOT):
                p = base / inp
                if p.exists():
                    try:
                        result[inp] = p.read_text(encoding="utf-8")
                    except Exception as e:
                        result[inp] = f"[ERRORE lettura: {e}]"
                    break
            else:
                result[inp] = f"[FILE NON TROVATO: {inp}]"
        return result

    def _build_system_prompt(self, step: dict, agent_content: str) -> str:
        return f"""Sei un agente temporaneo della AgentFactory. Esegui il seguente Agent Package con precisione.

{agent_content}

═══ REGOLE OPERATIVE ORCHESTRATORE ═══

- Leggi tutti gli input prima di agire.
- Produci SOLO gli output dichiarati nel task.
- Usa read_file per file aggiuntivi di cui hai bisogno.
- Usa write_file per scrivere gli output (percorso relativo al project workspace).
- Usa request_clarification SOLO per dubbi critici non risolvibili dagli input disponibili.
- Chiama complete_task al termine con stato e riepilogo dettagliato.

PERCORSI:
- Project workspace: {self.project_dir}
- write_file: percorso relativo al workspace (es. 'blueprints/requirements-blueprint.md')
- read_file: percorso relativo alla radice del repo (es. '{self.project_dir}/input/initial-request.md')
"""

    def _build_user_message(self, step: dict, inputs_content: dict) -> str:
        parts = [
            f"Esegui il task: **{step.get('name', step['id'])}**",
            f"Step ID: `{step['id']}`",
            "",
        ]
        if step.get("outputs"):
            parts.append("**Output attesi** (file da produrre):")
            for o in step["outputs"]:
                parts.append(f"- `{o}`")
            parts.append("")
        if inputs_content:
            parts.append("**Input disponibili:**\n")
            for path, content in inputs_content.items():
                parts.append(f"### {path}\n```\n{content}\n```\n")
        parts.append(
            "Procedi: analizza gli input, esegui il task, scrivi gli output con write_file, "
            "poi chiama complete_task con il riepilogo finale."
        )
        return "\n".join(parts)

    def run_agent(self, step: dict) -> tuple[bool, str, list]:
        """
        Run one agent step via Anthropic API agentic loop.
        Returns (success, summary, files_created).
        """
        step_id = step["id"]
        step_name = step.get("name", step_id)

        print(f"\n  → [{step_id}] {step_name}")

        agent_content = self._load_agent_content(step)
        inputs_content = self._load_inputs(step)
        system = self._build_system_prompt(step, agent_content)
        user_msg = self._build_user_message(step, inputs_content)

        messages = [{"role": "user", "content": user_msg}]
        completion_result = None
        tool_calls = 0

        while tool_calls < MAX_TOOL_CALLS:
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=8192,
                    system=system,
                    tools=TOOLS,
                    messages=messages,
                )
            except anthropic.APIError as e:
                print(f"     ✗ API error: {e}")
                return False, str(e), []

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                print("     ⚠ Agente terminato senza complete_task")
                return True, "Terminato senza riepilogo formale.", []

            if response.stop_reason != "tool_use":
                break

            tool_results = []
            done = False

            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_calls += 1
                name = block.name
                inp = block.input

                # Print compact tool call log (skip content for brevity)
                log_inp = {k: (repr(v)[:60] if k != "content" else f"<{len(v)} chars>")
                           for k, v in inp.items()}
                print(f"     🔧 {name}({', '.join(f'{k}={v}' for k, v in log_inp.items())})")

                result_str = self._execute_tool(name, inp)

                if name == "complete_task":
                    try:
                        completion_result = json.loads(result_str)
                    except Exception:
                        completion_result = inp
                    done = True

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_str,
                })

            messages.append({"role": "user", "content": tool_results})

            if done:
                break

        if tool_calls >= MAX_TOOL_CALLS:
            print(f"     ⚠ Limite tool call raggiunto ({MAX_TOOL_CALLS})")

        if completion_result:
            status = completion_result.get("status", "completed")
            summary = completion_result.get("summary", "")
            files = completion_result.get("files_created", [])
            success = status in ("completed", "changes-requested")
            icon = "✓" if success else "✗"
            print(f"     {icon} {status}")
            for line in summary.splitlines()[:4]:
                print(f"       {line}")
            if len(summary.splitlines()) > 4:
                print("       ...")
            return success, summary, files

        return False, "complete_task non chiamato.", []

    # ── Human Gate ────────────────────────────────────────────────────────────

    def check_human_gate(self, gate_id: str) -> bool:
        gate_file = self.project_dir / "human-gates" / f"{gate_id}.md"

        if not gate_file.exists():
            print(f"     ℹ Human Gate '{gate_id}' non trovato — skip")
            return True

        content = gate_file.read_text(encoding="utf-8")
        m = re.search(r"[-*]\s+status:\s*(.+)", content, re.IGNORECASE)
        status = m.group(1).strip().strip("`").lower() if m else "pending"

        if status == "approved":
            print(f"     ✓ Human Gate '{gate_id}': approvato")
            return True
        if status == "rejected":
            print(f"     ✗ Human Gate '{gate_id}': rifiutato — stop")
            return False
        if status == "cancelled":
            print(f"     ℹ Human Gate '{gate_id}': cancellato — proseguo")
            return True

        # Pending (or expired) — interactive
        print(f"\n{'━'*60}")
        print(f"  ⚠  HUMAN GATE PENDING: {gate_id}")
        print(f"{'━'*60}")
        print(f"  File: {gate_file}")

        while True:
            try:
                choice = input("\n  [a]pprova  [r]ifiuta  [v]iew  [s]kip: ").strip().lower()
            except EOFError:
                choice = "s"

            if choice == "v":
                print(f"\n{'─'*60}")
                print(content[:3000])
                if len(content) > 3000:
                    print(f"  ... (troncato — vedi {gate_file})")
                print(f"{'─'*60}")
            elif choice in ("a", "approva", "approve"):
                updated = re.sub(
                    r"([-*]\s+status:\s*)\S+",
                    r"\1Approved",
                    content,
                    flags=re.IGNORECASE,
                )
                if updated == content:
                    updated += f"\n- status: Approved\n- approved-at: {datetime.now().isoformat()}\n"
                gate_file.write_text(updated, encoding="utf-8")
                print(f"  ✓ Approvato — proseguo")
                return True
            elif choice in ("r", "rifiuta", "reject"):
                updated = re.sub(
                    r"([-*]\s+status:\s*)\S+",
                    r"\1Rejected",
                    content,
                    flags=re.IGNORECASE,
                )
                if updated == content:
                    updated += f"\n- status: Rejected\n- rejected-at: {datetime.now().isoformat()}\n"
                gate_file.write_text(updated, encoding="utf-8")
                print(f"  ✗ Rifiutato — stop")
                return False
            elif choice == "s":
                print("  ⚠ Skippato")
                return True
            else:
                print("  Scelta non valida. Usa: a, r, v, s")

    # ── Output validation ─────────────────────────────────────────────────────

    def _validate_outputs(self, step: dict) -> bool:
        outputs = [
            str(self.project_dir / o)
            for o in step.get("outputs", [])
            if (self.project_dir / o).exists()
        ]
        if not outputs:
            return True
        try:
            r = subprocess.run(
                [sys.executable, "tools/validate.py"] + outputs,
                capture_output=True,
                text=True,
            )
            if r.returncode != 0:
                for line in r.stdout.strip().splitlines()[-8:]:
                    print(f"     ! {line}")
            return r.returncode == 0
        except Exception:
            return True

    # ── Step execution ─────────────────────────────────────────────────────────

    def run_step(self, step: dict) -> bool:
        """Run a single sequential step: gate check, agent, validate, persist state."""
        step_id = step["id"]

        if step_id in self.state["completed"]:
            print(f"\n  ↷ [{step_id}] già completato — skip")
            return True

        if gate_id := step.get("human-gate"):
            if not self.check_human_gate(gate_id):
                self.state["failed"].append(step_id)
                self._save_state()
                return False

        success, summary, files = self.run_agent(step)
        self._validate_outputs(step)

        if success:
            self.state["completed"][step_id] = {
                "at": datetime.now().isoformat(),
                "summary": summary[:600],
                "files": files,
            }
        else:
            if step_id not in self.state["failed"]:
                self.state["failed"].append(step_id)

        self._save_state()
        return success

    async def run_parallel_group(self, parallel_steps: list) -> bool:
        ids = [s["id"] for s in parallel_steps]
        already_done = [s for s in parallel_steps if s["id"] in self.state["completed"]]
        to_run = [s for s in parallel_steps if s["id"] not in self.state["completed"]]

        if already_done and not to_run:
            print(f"\n  ↷ [parallelo] già completati — skip")
            return True

        print(f"\n  ⇉ Parallelo: {ids}")

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=len(to_run)) as executor:
            tasks = [loop.run_in_executor(executor, self.run_step, s) for s in to_run]
            results = await asyncio.gather(*tasks)

        return all(results)

    # ── Main run ───────────────────────────────────────────────────────────────

    async def run(self, from_step: str = None, dry_run: bool = False) -> bool:
        workflow = self.load_workflow()
        steps = workflow.get("steps", [])

        if not steps:
            print("Nessuno step trovato in workflow.yml.")
            return False

        if from_step:
            self.reset_from(from_step)

        print(f"\n{'━'*60}")
        print(f"  AgentFactory Orchestrator")
        print(f"  Progetto : {self.project_id}")
        print(f"  Modello  : {self.model}")
        if from_step:
            print(f"  Da step  : {from_step}")
        print(f"{'━'*60}")

        if dry_run:
            print("\n  Piano di esecuzione:\n")
            for i, item in enumerate(steps, 1):
                if "parallel" in item:
                    ids = " | ".join(s["id"] for s in item["parallel"])
                    print(f"  {i}. [parallelo] {ids}")
                else:
                    gate = f"  → gate: {item['human-gate']}" if item.get("human-gate") else ""
                    name = item.get("name", item["id"])
                    done = " ✓" if item["id"] in self.state["completed"] else ""
                    print(f"  {i}. {item['id']} — {name}{gate}{done}")
            print()
            return True

        for item in steps:
            if "parallel" in item:
                ok = await self.run_parallel_group(item["parallel"])
            else:
                ok = self.run_step(item)

            if not ok:
                step_id = item.get("id") or "[parallelo]"
                print(f"\n  ✗ Pipeline interrotta a '{step_id}'")
                print(f"  Per riprendere: python tools/orchestrate.py {self.project_id} --from <step-id>")
                self._print_summary()
                return False

        print(f"\n{'━'*60}")
        print(f"  ✓ Pipeline completata — {len(self.state['completed'])} step eseguiti")
        print(f"{'━'*60}\n")
        self._print_summary()
        return True

    def _print_summary(self):
        if not self.state["completed"]:
            return
        print("\n  Step completati:")
        for sid, info in self.state["completed"].items():
            print(f"    ✓ {sid}  ({info.get('at', '')[:16]})")
            for f in info.get("files", []):
                print(f"       • {f}")
        if self.state["failed"]:
            print("\n  Step falliti:")
            for sid in self.state["failed"]:
                print(f"    ✗ {sid}")
        print()


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="ID del progetto (cartella in projects/)")
    parser.add_argument(
        "--from", dest="from_step", metavar="STEP_ID",
        help="Riparte da questo step (resetta lo stato da quel punto in poi)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Mostra il piano di esecuzione senza eseguire agenti",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Modello Anthropic da usare (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    project_dir = PROJECTS_DIR / args.project_id
    if not project_dir.exists():
        print(f"ERRORE: progetto '{args.project_id}' non trovato in {PROJECTS_DIR}/", file=sys.stderr)
        sys.exit(1)

    orchestrator = Orchestrator(args.project_id, model=args.model)

    try:
        success = asyncio.run(
            orchestrator.run(from_step=args.from_step, dry_run=args.dry_run)
        )
    except FileNotFoundError as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n  Interrotto dall'utente. Lo stato è stato salvato.")
        print(f"  Riprendi con: python tools/orchestrate.py {args.project_id} --from <step-id>")
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
