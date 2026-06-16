# Project Workspace Template

Questo template definisce la struttura minima di un Project Workspace temporaneo.

## Uso

Copiare `projects/_template/` in `projects/<project-id>/` e aggiornare:

- `project-status.md`
- `factory-state.json`
- `artifact-index.md`
- file in `input/`
- blueprint in `blueprints/`
- summary approvate in `summaries/`
- Agent Package in `generated-agents/`
- runtime packet in `runtime-packets/`
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
- `factory-state.json` e la fonte compatta per riprendere il processo senza rileggere tutto il workspace.
- I runtime packet riducono il contesto passato agli agenti temporanei.

## Struttura

```text
projects/<project-id>/
|-- README.md
|-- project-status.md
|-- factory-state.json
|-- artifact-index.md
|-- input/
|-- blueprints/
|-- summaries/
|-- generated-agents/
|-- runtime-packets/
|-- handoffs/
|-- human-gates/
|-- deliverables/
|-- reviews/
`-- knowledge-candidates/
```
