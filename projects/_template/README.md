# Project Workspace Template

Questo template definisce la struttura minima di un Project Workspace temporaneo.

## Uso

Copiare `projects/_template/` in `projects/<project-id>/` e aggiornare:

- `project-status.md`
- file in `input/`
- blueprint in `blueprints/`
- Agent Package in `generated-agents/`
- handoff in `handoffs/`
- Human Gate in `human-gates/`
- deliverable in `deliverables/`
- review in `reviews/`
- Knowledge Candidate in `knowledge-candidates/`

## Regole

- Il Project Workspace contiene lavoro temporaneo, non conoscenza permanente approvata.
- Le Knowledge Candidate restano proposte finche Knowledge Evolution non le valuta.
- Un Human Gate `Pending` blocca il workflow nel proprio `blocking-scope`.
- Ogni passaggio tra agenti o fasi deve produrre handoff verificabile.
- I deliverable finali devono essere collegati ai criteri di accettazione.

## Struttura

```text
projects/<project-id>/
|-- README.md
|-- project-status.md
|-- input/
|-- blueprints/
|-- generated-agents/
|-- handoffs/
|-- human-gates/
|-- deliverables/
|-- reviews/
`-- knowledge-candidates/
```
