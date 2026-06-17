---
standard: agent-package
applies-to: "projects/[!_]*/generated-agents/*.md"
required-sections:
  - "## Metadata"
  - "## Mission"
  - "## Task"
  - "## Inputs"
  - "## Expected Outputs"
  - "## Responsibilities"
  - "## Boundaries"
  - "## Tools"
  - "## Workflow"
  - "## Handoff Requirements"
  - "## Definition of Done"
optional-sections:
  - "## Runtime Hints"
  - "## Risk Notes"
  - "## Review Gates"
  - "## Escalation Rules"
  - "## Knowledge Candidate Triggers"
---

# Agent Package Standard

## Scopo

Definire il formato minimo di un Agent Package temporaneo. Un Agent Package descrive un agente pronto per essere eseguito da un runtime adapter, senza dipendere da un runtime specifico.

## Creato da

Knowledge Compiler.

## Usato da

Runtime Adapter, Project Team, Pipeline Supervisor.

## Quando si usa

Si usa dopo l'approvazione di un Execution Blueprint, quando serve generare uno o piu agenti temporanei per un progetto o task.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `package-id` | Identificativo in kebab-case, unico nel progetto. |
| `project-id` | Identificativo del progetto workspace. |
| `agent-role` | Ruolo operativo dell'agente temporaneo. |
| `agent-source` | Sorgente del ruolo: archetype esistente o definizione ad hoc nell'Execution Blueprint. |
| `assigned-capabilities` | Elenco delle capability assegnate con percorso. |
| `mission` | Obiettivo specifico dell'agente in questo progetto. |
| `task` | Task assegnato, espresso in modo verificabile. |
| `inputs` | Artefatti, file, blueprint e vincoli disponibili. |
| `expected-outputs` | Deliverable richiesti. |
| `responsibilities` | Cosa l'agente deve fare. |
| `boundaries` | Cosa l'agente non deve fare. |
| `tools` | Tool disponibili o vietati. |
| `workflow` | Passi operativi minimi. |
| `handoff-requirements` | Handoff da produrre o consumare. |
| `definition-of-done` | Condizioni verificabili di completamento. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `chunk-id` | ID del chunk dell'Implementation Plan coperto da questo package (es. `auth-module`). Obbligatorio quando generato da un Implementation Plan. |
| `chunk-modules` | Lista dei moduli dell'Implementation Plan inclusi in questo package. |
| `chunk-dependencies` | Lista dei chunk-id che devono essere completati prima di eseguire questo package. |
| `runtime-hints` | Indicazioni non vincolanti per runtime adapter. |
| `runtime-packet` | Percorso del runtime packet compatto collegato al package, se generato. |
| `risk-notes` | Rischi specifici del task. |
| `review-gates` | Gate di review collegati all'agente. |
| `escalation-rules` | Quando fermarsi e chiedere supervisione. |
| `knowledge-candidate-triggers` | Situazioni in cui proporre Knowledge Candidate. |

## Formato consigliato

```markdown
# Agent Package: <package-id>

## Metadata

- package-id:
- project-id:
- agent-role:
- agent-source:
  - type:
  - reference:
- assigned-capabilities:

## Mission

## Task

## Inputs

## Expected Outputs

## Responsibilities

## Boundaries

## Tools

## Workflow

## Handoff Requirements

## Definition of Done

## Runtime Hints

## Runtime Packet

## Risk Notes

## Review Gates

## Escalation Rules

## Knowledge Candidate Triggers
```

## Criteri di validita

Un Agent Package e valido quando:

1. il ruolo deriva da un archetype esistente oppure da una definizione ad hoc presente nell'Execution Blueprint;
2. ogni capability assegnata e pertinente al task;
3. input e output sono verificabili;
4. responsabilita e limiti non si contraddicono;
5. la Definition of Done permette al Pipeline Supervisor di decidere se il task e completato;
6. il package non contiene conoscenza tecnica generica non necessaria al task;
7. il package non include decisioni strategiche non presenti nei blueprint;
8. se esiste un runtime packet, il package e il packet non si contraddicono.

## Failure mode

- Agent Package troppo lungo e pieno di contesto non operativo.
- Agent Package usato come unico contesto runtime quando un packet compatto sarebbe sufficiente.
- Capability assegnate solo per completezza, ma non usate dal task.
- Task non verificabile.
- Limiti assenti, con agente che invade responsabilita di altri ruoli.
- Runtime hints trasformati in logica decisionale.
- Definition of Done vaga o non misurabile.
- Archetype trattato come requisito obbligatorio anche quando serve un agente ad hoc.

## Esempio minimo

```markdown
# Agent Package: developer-node-api

## Metadata

- package-id: developer-node-api
- project-id: demo-api
- agent-role: Developer
- agent-source:
  - type: archetype
  - reference: archetypes/developer.md
- assigned-capabilities:
  - capabilities/node.md
  - capabilities/testing-strategy.md

## Mission

Implementare l'endpoint API definito nel Solution Blueprint.

## Task

Creare un endpoint `GET /health` che restituisca stato applicativo e timestamp.

## Inputs

- projects/demo-api/blueprints/requirements-blueprint.md
- projects/demo-api/blueprints/solution-blueprint.md
- projects/demo-api/blueprints/execution-blueprint.md

## Expected Outputs

- Codice endpoint.
- Test automatico dell'endpoint.
- Handoff verso Reviewer.

## Responsibilities

- Implementare il codice richiesto.
- Eseguire test pertinenti.
- Documentare decisioni operative.

## Boundaries

- Non cambiare architettura.
- Non aggiungere endpoint non richiesti.

## Tools

- Editor repository.
- Test runner disponibile nel progetto.

## Workflow

1. Leggere blueprint e capability.
2. Implementare il task.
3. Eseguire test.
4. Produrre handoff.

## Handoff Requirements

Produrre un handoff conforme a `standards/handoff-standard.md`.

## Definition of Done

- Endpoint implementato.
- Test eseguiti e riportati.
- Handoff creato.
```
