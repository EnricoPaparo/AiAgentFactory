# Knowledge Candidate Standard

## Scopo

Definire il formato minimo di una Knowledge Candidate. Una Knowledge Candidate e una proposta di miglioramento nata durante un progetto e non modifica automaticamente la conoscenza permanente.

## Creato da

Qualsiasi agente o fase.

## Usato da

Knowledge Evolution, Pipeline Supervisor, maintainer della factory.

## Quando si usa

Si usa quando durante un progetto emerge una regola, checklist, failure mode, capability, standard o adattamento che potrebbe essere riutilizzabile oltre il progetto corrente.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `candidate-id` | Identificativo in kebab-case, unico nel progetto. |
| `project-id` | Progetto da cui nasce la proposta. |
| `status` | Uno tra `Proposed`, `Reviewed`, `Accepted`, `Integrated`, `Rejected`, `Deprecated`. |
| `proposed-by` | Agente o fase che propone. |
| `target-area` | Destinazione proposta: archetype, capability, standard, agent, runtime adapter o process rule. |
| `proposal` | Modifica proposta. |
| `context` | Situazione concreta che ha generato la proposta. |
| `motivation` | Perche la proposta e utile. |
| `generalizability` | Quanto e riutilizzabile fuori dal progetto. |
| `risk` | Rischi di integrazione o uso improprio. |
| `recommended-action` | Azione suggerita. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `evidence` | Handoff, review, errori o risultati che supportano la proposta. |
| `review-notes` | Valutazione di Knowledge Evolution. |
| `decision` | Accettata, respinta, integrata o deprecata con motivazione. |
| `integration-target` | File permanente da modificare se accettata. |

## Formato consigliato

```markdown
# Knowledge Candidate: <candidate-id>

## Metadata

- candidate-id:
- project-id:
- status:
- proposed-by:
- target-area:

## Proposal

## Context

## Motivation

## Generalizability

## Risk

## Recommended Action

## Evidence

## Review Notes

## Decision

## Integration Target
```

## Criteri di validita

Una Knowledge Candidate e valida quando:

1. nasce da un caso concreto;
2. distingue conoscenza locale da conoscenza riutilizzabile;
3. dichiara rischi e generalizzabilita;
4. propone una destinazione plausibile;
5. non viene integrata senza review;
6. mantiene lo stato aggiornato.

## Failure mode

- Ogni preferenza locale viene trasformata in regola permanente.
- Proposta senza contesto o prova.
- Generalizzabilita non valutata.
- Stato saltato direttamente da `Proposed` a `Integrated`.
- Destinazione troppo generica.

## Esempio minimo

```markdown
# Knowledge Candidate: require-test-evidence-in-developer-handoff

## Metadata

- candidate-id: require-test-evidence-in-developer-handoff
- project-id: demo-api
- status: Proposed
- proposed-by: Reviewer
- target-area: standard

## Proposal

Rendere `test-evidence` obbligatorio negli handoff Developer to Reviewer.

## Context

Durante la review non era chiaro quali test fossero stati eseguiti.

## Motivation

Riduce ambiguita e velocizza la review.

## Generalizability

Alta per progetti software con test eseguibili.

## Risk

Potrebbe essere eccessivo per task puramente documentali.

## Recommended Action

Valutare aggiornamento di `standards/handoff-standard.md`.
```
