# Run Record Standard

## Scopo

Definire il formato minimo di un run record AgentFactory.

Un run record traccia una singola azione operativa: validazione, approval, generazione packet, esecuzione agente, review o supervisione. Serve a rendere auditabile cosa e stato fatto, con quali input, quali output e quale esito.

## Creato da

Factory Runner, Runtime Adapter, agente temporaneo o tool operativo.

## Usato da

Factory Runner, Pipeline Supervisor, Human Maintainer, Knowledge Evolution.

## Posizione

```text
projects/<project-id>/run-records/<timestamp>-<action>.md
```

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `record-id` | Identificativo unico del record. |
| `project-id` | Identificativo progetto. |
| `created-at` | Timestamp locale o ISO. |
| `actor` | Agente, runtime o tool che ha prodotto il record. |
| `action` | Azione eseguita. |
| `status` | `completed`, `blocked`, `failed`, `changes-requested` o `info`. |
| `inputs` | File e decisioni usate. |
| `outputs` | File prodotti o modificati. |
| `checks` | Verifiche eseguite. |
| `token-notes` | Note su contesto usato, packet e letture evitate. |
| `residual-risks` | Rischi o limiti residui. |

## Formato consigliato

```markdown
# Run Record: <record-id>

## Metadata

- record-id:
- project-id:
- created-at:
- actor:
- action:
- status:

## Inputs

## Outputs

## Checks

## Token Notes

## Residual Risks
```

## Regole

- Ogni approval gestita da CLI o runner deve creare un run record.
- Ogni esecuzione di Agent Package deve indicare se ha usato runtime packet o contesto completo.
- I run record non sostituiscono handoff e review report; li rendono auditabili.
- Pipeline Supervisor deve poter leggere i run record per capire cosa e stato verificato senza ricostruire tutta la conversazione.
