---
standard: human-gate
applies-to: "projects/[!_]*/human-gates/*.md"
required-sections:
  - "## Metadata"
  - "## Decision Required"
  - "## Context"
  - "## Options"
  - "## Approval Criteria"
  - "## Impact If Approved"
  - "## Impact If Rejected"
  - "## Human Decision"
optional-sections:
  - "## Return To Phase"
  - "## Blocking Scope"
---

# Human Gate Standard

## Scopo

Definire il formato minimo di un Human Gate. Un Human Gate e un punto di controllo in cui la factory deve fermarsi e attendere una decisione umana prima di continuare.

## Creato da

Pipeline Designer o Pipeline Supervisor.

## Usato da

Pipeline Supervisor, Runtime Adapter, Project Team, maintainer umano.

## Quando si usa

Si usa quando una decisione puo cambiare scope, costo, rischio, architettura, dati sensibili, rilascio in produzione o conoscenza permanente.

## Stati ammessi

| Stato | Significato |
|---|---|
| `Pending` | Decisione richiesta, processo bloccato sul gate. |
| `Approved` | Decisione approvata, il processo puo proseguire. |
| `Rejected` | Decisione respinta, il processo viene bloccato o chiuso. |
| `Changes Requested` | Sono richieste modifiche prima di ripresentare il gate. |
| `Cancelled` | Gate annullato perche non piu rilevante. |
| `Expired` | Gate non deciso entro il limite definito, se previsto. |

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `gate-id` | Identificativo in kebab-case, unico nel progetto. |
| `project-id` | Identificativo del progetto workspace. |
| `status` | Stato corrente del gate. |
| `requested-by` | Agente o fase che richiede il gate. |
| `decision-owner` | Persona o ruolo umano responsabile della decisione. |
| `decision-required` | Decisione richiesta, formulata in modo esplicito. |
| `context` | Artefatti e motivazione necessari per decidere. |
| `options` | Opzioni consentite per la decisione. |
| `approval-criteria` | Criteri per approvare. |
| `impact-if-approved` | Cosa accade se il gate viene approvato. |
| `impact-if-rejected` | Cosa accade se il gate viene respinto. |
| `human-decision` | Decisione, autore, data e note. Vuoto finche `Pending`. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `created-at` | Data di creazione del gate. |
| `decided-at` | Data di decisione. |
| `expires-at` | Scadenza, se applicabile. |
| `return-to-phase` | Fase a cui tornare se sono richieste modifiche. |
| `blocking-scope` | Parte del workflow bloccata dal gate. |

## Formato consigliato

```markdown
# Human Gate: <gate-id>

## Metadata

- gate-id:
- project-id:
- status:
- requested-by:
- decision-owner:
- created-at:
- decided-at:
- expires-at:

## Decision Required

## Context

## Options

## Approval Criteria

## Impact If Approved

## Impact If Rejected

## Return To Phase

## Blocking Scope

## Human Decision

- decision:
- decided-by:
- decided-at:
- notes:
```

## Criteri di validita

Un Human Gate e valido quando:

1. la decisione richiesta e chiara;
2. il decision owner e esplicito;
3. gli artefatti di contesto sono indicati;
4. lo stato e uno degli stati ammessi;
5. se lo stato e `Pending`, il workflow downstream resta bloccato;
6. se lo stato e `Approved`, la decisione umana contiene autore e data;
7. se lo stato e `Changes Requested` o `Rejected`, esiste una motivazione.

## Regola di attesa

Quando esiste un Human Gate `Pending`, nessun agente o runtime adapter deve eseguire task downstream inclusi nel `blocking-scope`. Il Pipeline Supervisor deve fermare il processo e chiedere la decisione umana.

## Failure Mode

- Gate umano trattato come semplice nota.
- Processo che continua con gate `Pending`.
- Decision owner assente.
- Approvazione senza criteri o contesto.
- Richiesta di modifiche senza indicare fase di ritorno.

## Esempio minimo

```markdown
# Human Gate: approve-solution-blueprint

## Metadata

- gate-id: approve-solution-blueprint
- project-id: demo-api
- status: Pending
- requested-by: Pipeline Supervisor
- decision-owner: Human Maintainer
- created-at:
- decided-at:
- expires-at:

## Decision Required

Approvare il Solution Blueprint prima della creazione dell'Execution Blueprint.

## Context

- Requirements Blueprint: projects/demo-api/blueprints/requirements-blueprint.md
- Solution Blueprint: projects/demo-api/blueprints/solution-blueprint.md

## Options

- Approved
- Changes Requested
- Rejected

## Approval Criteria

- La soluzione soddisfa i requisiti.
- I trade-off sono accettabili.
- I rischi tecnici sono comprensibili.

## Impact If Approved

Il Pipeline Designer puo creare l'Execution Blueprint.

## Impact If Rejected

Il progetto viene bloccato o riportato all'Architect.

## Return To Phase

Architect.

## Blocking Scope

Execution Blueprint generation.

## Human Decision

- decision:
- decided-by:
- decided-at:
- notes:
```
