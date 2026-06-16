# Factory State Standard

## Scopo

Definire lo stato macchina compatto di un Project Workspace AgentFactory.

`factory-state.json` serve a evitare che il runtime debba rileggere tutti i markdown per capire dove si trova il processo.

## Creato da

Factory Intake o Factory Runner.

## Usato da

Factory Runner, Factory Host, Runtime Adapter, Pipeline Supervisor.

## Posizione

```text
projects/<project-id>/factory-state.json
```

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `project_id` | Identificativo progetto. |
| `phase` | Stato corrente della macchina. |
| `status` | `active`, `blocked`, `waiting_for_human`, `completed` o `failed`. |
| `pending_gate` | Gate aperto che blocca la prossima azione, oppure `null`. |
| `next_action` | Prossima azione attesa. |
| `artifact_index` | Percorso dell'indice artefatti. |
| `approved_summaries` | Summaries approvate disponibili. |
| `runtime_packets` | Runtime packet disponibili per agenti temporanei. |
| `run_records` | Cartella o indice dei run record disponibili. |
| `updated_at` | Data ultimo aggiornamento. |

## Fasi ammesse

- `intake`
- `requirements`
- `requirements_approval`
- `solution`
- `solution_approval`
- `execution_plan`
- `execution_plan_approval`
- `agent_generation`
- `execution`
- `review`
- `supervision`
- `final_delivery_approval`
- `closed`

## Formato minimo

```json
{
  "project_id": "project-id",
  "phase": "requirements_approval",
  "status": "waiting_for_human",
  "pending_gate": "approve-requirements",
  "next_action": "wait_for_human_approval",
  "artifact_index": "artifact-index.md",
  "approved_summaries": [],
  "runtime_packets": [],
  "run_records": "run-records/",
  "updated_at": "YYYY-MM-DD"
}
```

## Regole

- `pending_gate` deve essere `null` se `status` non e `waiting_for_human`.
- `next_action` deve essere abbastanza esplicita da permettere al Factory Runner di riprendere senza inferenza larga.
- Le summaries diventano `approved_summaries` solo dopo il gate corrispondente.
- I runtime packet devono essere rigenerati quando cambia l'Execution Blueprint o viene richiesto un cambio gate.
- Le approval gestite dal runner devono creare un run record.
- `project-status.md` resta leggibile per l'umano; `factory-state.json` e la fonte compatta per il runtime.
