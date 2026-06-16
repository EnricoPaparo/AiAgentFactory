# Runtime Packet Standard

## Scopo

Definire il formato minimo di un runtime packet: un contesto compatto, task-specifico e token-efficient per eseguire un Agent Package senza rileggere tutta la factory.

## Creato da

Knowledge Compiler o Factory Runner.

## Usato da

Runtime Adapter, agenti temporanei, Reviewer, Pipeline Supervisor.

## Posizione

```text
projects/<project-id>/runtime-packets/<packet-id>.json
```

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `packet_id` | Identificativo in kebab-case. |
| `project_id` | Identificativo progetto. |
| `agent_package` | Percorso dell'Agent Package completo. |
| `agent_role` | Ruolo dell'agente temporaneo. |
| `context_budget` | `low`, `medium` o `high`. |
| `task` | Task operativo sintetico. |
| `approved_context` | Summaries o blueprint approvate necessarie. |
| `required_files` | File che l'agente deve leggere. |
| `must_not` | Vincoli negativi compatti. |
| `expected_outputs` | Output richiesti. |
| `handoff_required` | Handoff da produrre. |
| `gate_status` | Gate che autorizzano o bloccano il task. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `fallback_full_context` | File lunghi da leggere solo se il packet non basta. |
| `verification_commands` | Comandi o controlli consigliati. |
| `review_focus` | Aspetti da verificare in review. |
| `token_notes` | Note per limitare contesto e riletture. |

## Formato minimo

```json
{
  "packet_id": "website-builder",
  "project_id": "demo-site",
  "agent_package": "generated-agents/website-builder-agent-package.md",
  "agent_role": "Website Builder",
  "context_budget": "low-medium",
  "task": "Implement landing page and contact page.",
  "approved_context": [
    "summaries/requirements-summary.md",
    "summaries/solution-summary.md",
    "summaries/execution-summary.md"
  ],
  "required_files": [],
  "must_not": [
    "Do not invent realistic contact details."
  ],
  "expected_outputs": [
    "deliverables/site/index.html",
    "deliverables/site/contact.html"
  ],
  "handoff_required": "handoffs/website-builder-to-reviewer.md",
  "gate_status": {
    "approve-execution-plan": "Approved"
  }
}
```

## Regole

- Il runtime packet non sostituisce l'Agent Package completo; lo comprime per l'esecuzione.
- L'agente legge prima il packet, poi solo i file indicati.
- `fallback_full_context` si usa solo se manca un dettaglio necessario.
- Un packet non deve contenere decisioni non approvate nei blueprint.
- Se un gate torna a `Changes Requested`, i packet downstream diventano stale.
