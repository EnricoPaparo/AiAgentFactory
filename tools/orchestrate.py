#!/usr/bin/env python3
"""
Orchestratore AgentFactory.

Legge workflow.yml dal project workspace ed esegue automaticamente la pipeline
di agenti AI: step sequenziali, step paralleli, Human Gate interattivi,
chiarimenti all'utente, validazione output e ripresa da uno step specifico.

Supporta qualsiasi provider AI tramite due backend:
  - anthropic SDK  : per modelli Claude  (ANTHROPIC_API_KEY)
  - openai SDK     : per tutto il resto  (endpoint OpenAI-compatibili)

Provider gratuiti supportati:
  gemini/gemini-2.0-flash         → GEMINI_API_KEY   (aistudio.google.com)
  groq/llama-3.3-70b-versatile    → GROQ_API_KEY     (console.groq.com)
  ollama/llama3.1                 → nessuna chiave   (server locale)
  mistral/mistral-small-latest    → MISTRAL_API_KEY  (console.mistral.ai)

Uso:
  python tools/orchestrate.py <project-id>
  python tools/orchestrate.py <project-id> --model gemini/gemini-2.0-flash
  python tools/orchestrate.py <project-id> --model groq/llama-3.3-70b-versatile
  python tools/orchestrate.py <project-id> --model ollama/llama3.1
  python tools/orchestrate.py <project-id> --from <step-id>
  python tools/orchestrate.py <project-id> --dry-run
"""

import os
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
    print("ERRORE: PyYAML richiesto. Installa con: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

PROJECTS_DIR = Path("projects")
REPO_ROOT = Path(".")
DEFAULT_MODEL = "claude-opus-4-8"
MAX_TOOL_CALLS = 40

# Provider OpenAI-compatibili: prefisso → (base_url, variabile_env_api_key)
_OPENAI_PROVIDERS: dict[str, tuple[str, str | None]] = {
    "gemini":     ("https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY"),
    "groq":       ("https://api.groq.com/openai/v1",                          "GROQ_API_KEY"),
    "ollama":     ("http://localhost:11434/v1",                                None),
    "mistral":    ("https://api.mistral.ai/v1",                               "MISTRAL_API_KEY"),
    "together":   ("https://api.together.xyz/v1",                             "TOGETHER_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1",                            "OPENROUTER_API_KEY"),
}

# Tool in formato OpenAI function calling (usato dal backend openai).
# Il backend anthropic li converte automaticamente al formato Anthropic.
TOOLS_OPENAI = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": (
                "Leggi il contenuto di un file. Usa percorsi relativi alla radice del repository. "
                "Esempi: 'projects/mio-progetto/input/initial-request.md', "
                "'standards/agent-package-standard.md'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Percorso relativo alla radice del repository."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Crea o sovrascrive un file nel project workspace. "
                "Percorso relativo al project workspace "
                "(es. 'blueprints/requirements-blueprint.md'). "
                "Le directory intermedie vengono create automaticamente."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path":    {"type": "string", "description": "Percorso relativo al project workspace."},
                    "content": {"type": "string", "description": "Contenuto completo del file."},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Elenca file e directory in un percorso del repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Percorso relativo alla radice del repo. Se omesso, elenca il project workspace.",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_clarification",
            "description": (
                "Poni domande all'utente umano per dubbi critici non risolvibili dagli input. "
                "L'esecuzione si mette in pausa finché l'utente non risponde. "
                "Usa solo per dubbi bloccanti — non per conferme di routine."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "questions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Lista di domande da porre all'utente.",
                    },
                    "context": {
                        "type": "string",
                        "description": "Contesto che spiega perché queste domande sono necessarie.",
                    },
                },
                "required": ["questions"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": (
                "Dichiara il completamento del task. Chiama SEMPRE questo tool al termine, "
                "sia in caso di successo che di blocco o fallimento."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["completed", "blocked", "changes-requested", "failed"],
                        "description": (
                            "completed=output prodotti; blocked=input mancante o Human Gate; "
                            "changes-requested=review richiede modifiche; failed=task non completabile."
                        ),
                    },
                    "summary": {
                        "type": "string",
                        "description": "Riepilogo: cosa fatto, file prodotti, rischi residui, prossimo agente.",
                    },
                    "files_created": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "File creati o modificati (percorsi relativi al project workspace).",
                    },
                },
                "required": ["status", "summary"],
            },
        },
    },
]

# Conversione in formato Anthropic per il backend anthropic SDK
TOOLS_ANTHROPIC = [
    {
        "name":         t["function"]["name"],
        "description":  t["function"]["description"],
        "input_schema": t["function"]["parameters"],
    }
    for t in TOOLS_OPENAI
]


# ── Risposta normalizzata ──────────────────────────────────────────────────────

class _ToolCall:
    def __init__(self, name: str, call_id: str, arguments: dict):
        self.name = name
        self.call_id = call_id
        self.arguments = arguments

class _NormalizedResponse:
    def __init__(self, text: str | None, tool_calls: list[_ToolCall]):
        self.text = text
        self.tool_calls = tool_calls

    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)


# ── Creazione client ───────────────────────────────────────────────────────────

def _make_client(model: str):
    """
    Restituisce (backend, client, model_name).
    backend è 'anthropic' o 'openai'.
    """
    # Claude → anthropic SDK
    if model.startswith("claude-") or model.startswith("anthropic/"):
        try:
            import anthropic
        except ImportError:
            print("ERRORE: pip install anthropic", file=sys.stderr)
            sys.exit(1)
        return "anthropic", anthropic.Anthropic(), model.replace("anthropic/", "")

    # Provider OpenAI-compatibile
    try:
        from openai import OpenAI
    except ImportError:
        print("ERRORE: pip install openai", file=sys.stderr)
        sys.exit(1)

    if "/" in model:
        provider, model_name = model.split("/", 1)
    else:
        provider, model_name = "openai", model

    if provider in _OPENAI_PROVIDERS:
        base_url, key_env = _OPENAI_PROVIDERS[provider]
        api_key = os.environ.get(key_env, "dummy") if key_env else "ollama"
        if key_env and not os.environ.get(key_env):
            print(f"ATTENZIONE: variabile {key_env} non impostata.", file=sys.stderr)
        client = OpenAI(api_key=api_key, base_url=base_url)
    else:
        client = OpenAI()  # OpenAI standard con OPENAI_API_KEY
        model_name = model

    return "openai", client, model_name


class Orchestrator:
    def __init__(self, project_id: str, model: str = DEFAULT_MODEL):
        self.project_id = project_id
        self.project_dir = PROJECTS_DIR / project_id
        self.model_str = model
        self.state_file = self.project_dir / ".orchestrator-state.json"
        self.state = self._load_state()
        self._clarification_lock = threading.Lock()
        self._backend, self._client, self._model_name = _make_client(model)

    # ── Stato ─────────────────────────────────────────────────────────────────

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
        """Rimuove from_step e tutti gli step successivi dallo stato completato."""
        all_ids = self._collect_step_ids(self.load_workflow().get("steps", []))
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

    # ── Caricamento workflow ───────────────────────────────────────────────────

    def load_workflow(self) -> dict:
        wf = self.project_dir / "blueprints" / "workflow.yml"
        if not wf.exists():
            raise FileNotFoundError(
                f"workflow.yml non trovato: {wf}\n"
                "Crea il file seguendo il template in projects/_template/blueprints/workflow.yml"
            )
        return yaml.safe_load(wf.read_text(encoding="utf-8"))

    # ── Chiamata API con normalizzazione ───────────────────────────────────────

    def _call_api(self, system: str, messages: list) -> _NormalizedResponse:
        if self._backend == "anthropic":
            response = self._client.messages.create(
                model=self._model_name,
                max_tokens=16000,
                system=system,
                tools=TOOLS_ANTHROPIC,
                messages=messages,
            )
            text = None
            tool_calls = []
            for block in response.content:
                if block.type == "text":
                    text = block.text
                elif block.type == "tool_use":
                    tool_calls.append(_ToolCall(block.name, block.id, block.input))
            if response.stop_reason == "max_tokens" and not text and not tool_calls:
                return _NormalizedResponse(
                    "RISPOSTA TRONCATA: max_tokens raggiunto. Riscrivi il file con contenuto più conciso.", []
                )
            return _NormalizedResponse(text, tool_calls)
        else:
            msgs = [{"role": "system", "content": system}] + messages
            response = self._client.chat.completions.create(
                model=self._model_name,
                max_tokens=8192,
                tools=TOOLS_OPENAI,
                messages=msgs,
            )
            msg = response.choices[0].message
            tool_calls = []
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    try:
                        inp = json.loads(tc.function.arguments)
                    except Exception:
                        inp = {}
                    tool_calls.append(_ToolCall(tc.function.name, tc.id, inp))
            return _NormalizedResponse(msg.content, tool_calls)

    def _append_assistant(self, messages: list, norm: _NormalizedResponse):
        """Aggiunge la risposta dell'assistente alla storia messaggi nel formato corretto."""
        if self._backend == "anthropic":
            content = []
            if norm.text:
                content.append({"type": "text", "text": norm.text})
            for tc in norm.tool_calls:
                content.append({"type": "tool_use", "id": tc.call_id, "name": tc.name, "input": tc.arguments})
            messages.append({"role": "assistant", "content": content})
        else:
            entry: dict = {"role": "assistant", "content": norm.text or ""}
            if norm.tool_calls:
                entry["tool_calls"] = [
                    {"id": tc.call_id, "type": "function",
                     "function": {"name": tc.name, "arguments": json.dumps(tc.arguments)}}
                    for tc in norm.tool_calls
                ]
            messages.append(entry)

    def _append_tool_result(self, messages: list, tc: _ToolCall, result: str):
        """Aggiunge il risultato di un tool alla storia messaggi nel formato corretto."""
        if self._backend == "anthropic":
            # Raggruppa i tool_result in un unico messaggio user
            if messages and messages[-1]["role"] == "user" and isinstance(messages[-1]["content"], list):
                messages[-1]["content"].append(
                    {"type": "tool_result", "tool_use_id": tc.call_id, "content": result}
                )
            else:
                messages.append({"role": "user", "content": [
                    {"type": "tool_result", "tool_use_id": tc.call_id, "content": result}
                ]})
        else:
            messages.append({"role": "tool", "tool_call_id": tc.call_id, "content": result})

    # ── Gestori tool ───────────────────────────────────────────────────────────

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
            lines = [
                f"  {item.name}{'/' if item.is_dir() else ''}"
                for item in sorted(target.iterdir())
            ]
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

    def _execute_tool(self, tc: _ToolCall) -> str:
        if tc.name == "read_file":
            return self._tool_read_file(tc.arguments["path"])
        if tc.name == "write_file":
            if "content" not in tc.arguments:
                return "ERRORE: argomento 'content' mancante. Richiama write_file includendo il parametro content con il contenuto completo del file."
            return self._tool_write_file(tc.arguments["path"], tc.arguments["content"])
        if tc.name == "list_files":
            return self._tool_list_files(tc.arguments.get("path"))
        if tc.name == "request_clarification":
            return self._tool_request_clarification(
                tc.arguments["questions"], tc.arguments.get("context")
            )
        if tc.name == "complete_task":
            return "Task registrato."
        return f"ERRORE: tool sconosciuto: {tc.name}"

    # ── Esecuzione agente ──────────────────────────────────────────────────────

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
        Esegue uno step agente tramite API con tool use.
        Restituisce (successo, riepilogo, file_creati).
        """
        step_id = step["id"]
        step_name = step.get("name", step_id)
        print(f"\n  → [{step_id}] {step_name}")

        agent_content = self._load_agent_content(step)
        inputs_content = self._load_inputs(step)
        system = self._build_system_prompt(step, agent_content)
        user_msg = self._build_user_message(step, inputs_content)

        messages: list = [{"role": "user", "content": user_msg}]
        completion_result = None
        tool_calls_count = 0

        while tool_calls_count < MAX_TOOL_CALLS:
            try:
                norm = self._call_api(system, messages)
            except Exception as e:
                print(f"     ✗ Errore API ({type(e).__name__}): {e}")
                return False, str(e), []

            self._append_assistant(messages, norm)

            if not norm.has_tool_calls:
                print("     ⚠ Agente terminato senza complete_task")
                return True, norm.text or "Terminato senza riepilogo formale.", []

            done = False
            for tc in norm.tool_calls:
                tool_calls_count += 1

                # Log compatto (omette il corpo di 'content')
                log_args = {
                    k: (repr(v)[:60] if k != "content" else f"<{len(str(v))} chars>")
                    for k, v in tc.arguments.items()
                }
                print(f"     🔧 {tc.name}({', '.join(f'{k}={v}' for k, v in log_args.items())})")

                if tc.name == "complete_task":
                    completion_result = tc.arguments
                    done = True

                result_str = self._execute_tool(tc)
                self._append_tool_result(messages, tc, result_str)

            if done:
                break

        if tool_calls_count >= MAX_TOOL_CALLS:
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

    def _create_gate_file(self, gate_id: str, gate_file) -> str:
        """Crea un file di gate minimale conforme allo standard se non esiste."""
        content = f"""# Human Gate: {gate_id}

## Metadata

- gate-id: {gate_id}
- project-id: {self.project_id}
- status: Pending
- requested-by: orchestratore (gate dichiarato nel workflow ma file non trovato)
- decision-owner: maintainer umano

## Decision Required

Approvare il proseguimento del progetto oltre il gate `{gate_id}`.

## Context

Il workflow dichiara un Human Gate `{gate_id}` ma il file corrispondente non era presente.
Questo gate è stato creato automaticamente dall'orchestratore in stato Pending.
Rivedere gli artefatti prodotti fino a questo punto prima di approvare.

## Options

- Approva: il workflow prosegue allo step successivo.
- Rifiuta: il workflow si ferma qui.

## Approval Criteria

- Gli artefatti prodotti fino a questo punto sono corretti e completi.
- Non ci sono rischi bloccanti da risolvere prima di continuare.

## Impact If Approved

Il workflow prosegue allo step successivo.

## Impact If Rejected

Il workflow si ferma. Rivedere e correggere gli artefatti prima di rilanciare.

## Human Decision

- decision: (da compilare)
- note: (da compilare)
- decided-at: (da compilare)
"""
        gate_file.parent.mkdir(parents=True, exist_ok=True)
        gate_file.write_text(content, encoding="utf-8")
        return content

    def check_human_gate(self, gate_id: str) -> bool:
        gate_file = self.project_dir / "human-gates" / f"{gate_id}.md"

        if not gate_file.exists():
            print(f"     ⚠ Human Gate '{gate_id}' non trovato — creo file Pending e blocco")
            content = self._create_gate_file(gate_id, gate_file)
            self._run_interactive_gate(gate_id, gate_file, content)
            content = gate_file.read_text(encoding="utf-8")
            m = re.search(r"[-*]\s+status:\s*(.+)", content, re.IGNORECASE)
            status = m.group(1).strip().strip("`").lower() if m else "pending"
            return status in ("approved", "cancelled")

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

        # Pending o expired — interattivo
        return self._run_interactive_gate(gate_id, gate_file, content)

    def _run_interactive_gate(self, gate_id: str, gate_file, content: str) -> bool:
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
            elif choice in ("a", "approva"):
                updated = re.sub(r"([-*]\s+status:\s*)\S+", r"\1Approved", content, flags=re.IGNORECASE)
                if updated == content:
                    updated += f"\n- status: Approved\n- approvato-il: {datetime.now().isoformat()}\n"
                gate_file.write_text(updated, encoding="utf-8")
                print("  ✓ Approvato — proseguo")
                return True
            elif choice in ("r", "rifiuta"):
                updated = re.sub(r"([-*]\s+status:\s*)\S+", r"\1Rejected", content, flags=re.IGNORECASE)
                if updated == content:
                    updated += f"\n- status: Rejected\n- rifiutato-il: {datetime.now().isoformat()}\n"
                gate_file.write_text(updated, encoding="utf-8")
                print("  ✗ Rifiutato — stop")
                return False
            elif choice == "s":
                print("  ⚠ Saltato (skip esplicito)")
                return True
            else:
                print("  Scelta non valida. Usa: a, r, v, s")

    # ── Validazione output ─────────────────────────────────────────────────────

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
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                for line in r.stdout.strip().splitlines()[-8:]:
                    print(f"     ! {line}")
            return r.returncode == 0
        except Exception:
            return True

    # ── Esecuzione step ────────────────────────────────────────────────────────

    def run_step(self, step: dict) -> bool:
        """Esegue uno step sequenziale: verifica gate, agente, validazione, salvataggio stato."""
        step_id = step["id"]

        if step_id in self.state["completed"]:
            print(f"\n  ↷ [{step_id}] già completato — salto")
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
        to_run = [s for s in parallel_steps if s["id"] not in self.state["completed"]]

        if not to_run:
            print(f"\n  ↷ [parallelo] già completati — salto")
            return True

        print(f"\n  ⇉ Parallelo: {ids}")

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=len(to_run)) as executor:
            tasks = [loop.run_in_executor(executor, self.run_step, s) for s in to_run]
            results = await asyncio.gather(*tasks)

        return all(results)

    # ── Esecuzione principale ──────────────────────────────────────────────────

    async def run(self, from_step: str = None, dry_run: bool = False) -> bool:
        workflow = self.load_workflow()
        steps = workflow.get("steps", [])

        if not steps:
            print("Nessuno step trovato in workflow.yml.")
            return False

        if from_step:
            self.reset_from(from_step)

        print(f"\n{'━'*60}")
        print(f"  AgentFactory Orchestratore")
        print(f"  Progetto : {self.project_id}")
        print(f"  Modello  : {self.model_str}")
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
            ok = (
                await self.run_parallel_group(item["parallel"])
                if "parallel" in item
                else self.run_step(item)
            )
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
        self._validate_project()
        return True

    def _validate_project(self):
        """Esegue validate.py su tutti gli artefatti del progetto e stampa il report."""
        artifacts = sorted(self.project_dir.rglob("*.md"))
        artifacts = [str(p) for p in artifacts if p.name != "README.md"]
        if not artifacts:
            return
        print(f"{'─'*60}")
        print(f"  Validazione artefatti progetto\n")
        try:
            r = subprocess.run(
                [sys.executable, "tools/validate.py"] + artifacts,
                capture_output=True, text=True,
            )
            for line in r.stdout.strip().splitlines():
                print(f"  {line}")
        except Exception as e:
            print(f"  ⚠ validate.py non disponibile: {e}")
        print()

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


# ── Interfaccia a riga di comando ─────────────────────────────────────────────

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
        help=(
            f"Modello da usare (default: {DEFAULT_MODEL}). "
            "Esempi: gemini/gemini-2.0-flash  groq/llama-3.3-70b-versatile  ollama/llama3.1"
        ),
    )
    args = parser.parse_args()

    if not (PROJECTS_DIR / args.project_id).exists():
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
