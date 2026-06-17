---
standard: execution-blueprint
applies-to: "projects/*/blueprints/execution-blueprint.md"
required-sections:
  - "## Requirements Source"
  - "## Solution Source"
  - "## Execution Goal"
  - "## Required Agents"
  - "## Agent Inputs"
  - "## Agent Outputs"
  - "## Workflow"
  - "## Handoffs"
  - "## Review Gates"
  - "## Human Gates"
  - "## Completion Criteria"
  - "## Escalation Rules"
optional-sections:
  - "## Parallelization Notes"
  - "## Runtime Preferences"
  - "## Knowledge Candidate Plan"
  - "## Workflow Yml"
---

# Execution Blueprint Standard

## Scopo

Definire il formato minimo dell'Execution Blueprint. Questo artefatto trasforma requisiti e soluzione in una pipeline operativa con agenti, workflow, handoff, review gate, human gate e criteri di completamento.

## Creato da

Pipeline Designer.

## Usato da

Knowledge Compiler, Pipeline Supervisor, Project Team.

## Quando si usa

Si usa dopo Requirements Blueprint e Solution Blueprint validi, prima della generazione degli Agent Package.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `project-id` | Identificativo del progetto. |
| `requirements-source` | Percorso del Requirements Blueprint. |
| `solution-source` | Percorso del Solution Blueprint. |
| `execution-goal` | Obiettivo operativo della pipeline. |
| `required-agents` | Agenti temporanei richiesti con ruolo, sorgente e motivazione. La sorgente puo essere `archetype` o `ad-hoc-definition`. |
| `agent-inputs` | Input assegnati a ciascun agente. |
| `agent-outputs` | Output attesi da ciascun agente. |
| `workflow` | Sequenza di lavoro. |
| `handoffs` | Handoff richiesti tra fasi o agenti. |
| `review-gates` | Controlli obbligatori e responsabili. |
| `human-gates` | Punti in cui la pipeline deve fermarsi e attendere validazione umana. Usare `None` se assenti. |
| `completion-criteria` | Criteri di completamento del progetto. |
| `escalation-rules` | Condizioni di blocco o richiesta supervisione. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `parallelization-notes` | Task eseguibili in parallelo. |
| `runtime-preferences` | Preferenze non vincolanti per runtime adapter. |
| `knowledge-candidate-plan` | Dove raccogliere lezioni e proposte. |
| `workflow-yml` | Riferimento al file `blueprints/workflow.yml` generato contestualmente, consumato da `tools/orchestrate.py`. |

## Formato consigliato

```markdown
# Execution Blueprint: <project-id>

## Requirements Source

## Solution Source

## Execution Goal

## Required Agents

## Agent Inputs

## Agent Outputs

## Workflow

## Handoffs

## Review Gates

## Human Gates

## Completion Criteria

## Escalation Rules

## Parallelization Notes

## Runtime Preferences

## Knowledge Candidate Plan

## Workflow Yml
```

## Criteri di validita

Un Execution Blueprint e valido quando:

1. ogni agente richiesto ha una responsabilita distinta;
2. ogni output richiesto ha almeno un agente responsabile;
3. ogni handoff ha mittente, destinatario e condizione di verifica;
4. i review gate sono eseguibili, non solo dichiarati;
5. i criteri di completamento si collegano ai criteri di accettazione;
6. non aggiorna conoscenza permanente direttamente;
7. non contiene dettagli runtime-specifici obbligatori;
8. ogni agente dichiara se deriva da archetype o da definizione ad hoc;
9. ogni Human Gate dichiara decisione richiesta, decision owner e blocking scope;
10. nessun task downstream dipende da Human Gate `Pending`.
11. per un progetto software end-to-end include almeno il gate `approve-execution-plan` prima di generare Agent Package e il gate `approve-final-delivery` prima della chiusura.

## Failure mode

- Troppi agenti per un task semplice.
- Responsabilita sovrapposte tra agenti.
- Review gate non assegnati.
- Human gate necessario ma non dichiarato.
- Workflow che prosegue nonostante Human Gate `Pending`.
- Handoff mancanti tra implementazione e review.
- Pipeline legata prematuramente a un runtime.

## Esempio minimo

```markdown
# Execution Blueprint: demo-api

## Requirements Source

projects/demo-api/blueprints/requirements-blueprint.md

## Solution Source

projects/demo-api/blueprints/solution-blueprint.md

## Execution Goal

Implementare e verificare endpoint `GET /health`.

## Required Agents

- Developer: implementa endpoint e test.
- Reviewer: verifica codice, test e handoff.

Sorgenti:

- Developer: archetype `archetypes/developer.md`.
- Reviewer: archetype `archetypes/reviewer.md`.

## Agent Inputs

- Developer: requirements, solution, repository.
- Reviewer: handoff Developer, diff, test evidence.

## Agent Outputs

- Developer: codice, test, handoff.
- Reviewer: review report.

## Workflow

1. Generare Agent Package Developer.
2. Eseguire implementazione.
3. Produrre handoff.
4. Generare Agent Package Reviewer.
5. Eseguire review.

## Handoffs

- Developer to Reviewer.

## Review Gates

- Code review.
- Test evidence review.

## Human Gates

- approve-execution-plan: validazione umana del team di agenti, workflow, handoff, review gate e piano operativo prima della generazione degli Agent Package.
- approve-final-delivery: validazione umana prima della chiusura progetto.

## Completion Criteria

- Deliverable presente.
- Test riportati.
- Review completata.

## Escalation Rules

Bloccare se lo stack non e identificabile.
```
