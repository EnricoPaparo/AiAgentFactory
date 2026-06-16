# Project Bootstrap Standard

## Scopo

Definire il formato minimo del bootstrap di un nuovo progetto AgentFactory. Il bootstrap trasforma una richiesta grezza dell'utente in un Project Workspace pronto per eseguire il Requirement Analyst.

## Creato da

Factory Intake.

## Usato da

Requirement Analyst, Pipeline Supervisor, Runtime Adapter, maintainer umano.

## Quando si usa

Si usa quando un utente fornisce una nuova idea di progetto e la factory deve creare il workspace iniziale senza richiedere all'utente di scrivere manualmente blueprint o Agent Package.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `project-id` | Identificativo in kebab-case generato dalla richiesta. |
| `source-request` | Richiesta utente originale preservata. |
| `workspace-path` | Percorso del Project Workspace creato. |
| `initial-request-path` | Percorso del file con la richiesta iniziale. |
| `factory-state-path` | Percorso dello stato macchina compatto. |
| `artifact-index-path` | Percorso dell'indice artefatti. |
| `bootstrap-execution-blueprint-path` | Percorso del blueprint minimo per avviare Requirement Analyst. |
| `first-agent-package-path` | Percorso dell'Agent Package del Requirement Analyst. |
| `human-gates` | Human Gate iniziali, se necessari. |
| `next-runtime-prompt` | Prompt o istruzioni per avviare il primo agente. |

## Output minimi

Un bootstrap valido crea almeno:

```text
projects/<project-id>/
|-- README.md
|-- project-status.md
|-- factory-state.json
|-- artifact-index.md
|-- input/initial-request.md
|-- blueprints/bootstrap-execution-blueprint.md
|-- generated-agents/requirement-analyst-agent-package.md
|-- human-gates/approve-requirements.md
|-- handoffs/
|-- deliverables/
|-- reviews/
`-- knowledge-candidates/
```

## Criteri di validita

Un Project Bootstrap e valido quando:

1. la richiesta utente e preservata senza riscrittura sostanziale;
2. il `project-id` e stabile, descrittivo e in kebab-case;
3. il workspace contiene tutte le cartelle minime;
4. `factory-state.json` dichiara fase e prossima azione senza richiedere inferenza larga;
5. `artifact-index.md` elenca gli artefatti iniziali;
6. il primo Agent Package puo essere eseguito con un runtime adapter;
7. il bootstrap non sceglie architettura, stack o piano operativo completo;
8. eventuali Human Gate iniziali dichiarano status, decision owner e blocking scope;
9. il prossimo passo e chiaro per l'utente o per il runtime.

## Failure Mode

- Factory Intake diventa un super-agente che produce requisiti, architettura e piano completo.
- La richiesta originale viene riscritta perdendo intenzione o vincoli.
- Il bootstrap sceglie stack o soluzione tecnica.
- Manca il primo Agent Package eseguibile.
- Human Gate iniziali bloccano il primo agente per errore.
- Il workspace viene creato senza stato progetto o senza handoff directory.

## Esempio minimo

```markdown
# Project Bootstrap: simple-landing-page

## Metadata

- project-id: simple-landing-page
- workspace-path: projects/simple-landing-page
- source-request: input/initial-request.md
- factory-state: projects/simple-landing-page/factory-state.json
- artifact-index: projects/simple-landing-page/artifact-index.md

## Created Artifacts

- projects/simple-landing-page/input/initial-request.md
- projects/simple-landing-page/factory-state.json
- projects/simple-landing-page/artifact-index.md
- projects/simple-landing-page/blueprints/bootstrap-execution-blueprint.md
- projects/simple-landing-page/generated-agents/requirement-analyst-agent-package.md
- projects/simple-landing-page/human-gates/approve-requirements.md

## Next Action

Run Requirement Analyst with `runtime-adapters/codex.md`.
```
