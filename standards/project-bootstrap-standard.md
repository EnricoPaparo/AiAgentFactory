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
4. il primo Agent Package puo essere eseguito con un runtime adapter;
5. il bootstrap non sceglie architettura, stack o piano operativo completo;
6. eventuali Human Gate iniziali dichiarano status, decision owner e blocking scope;
7. il prossimo passo e chiaro per l'utente o per il runtime.

## Failure Mode

- Factory Intake diventa un super-agente che produce requisiti, architettura e piano completo.
- La richiesta originale viene riscritta perdendo intenzione o vincoli.
- Il bootstrap sceglie stack o soluzione tecnica.
- Manca il primo Agent Package eseguibile.
- Human Gate iniziali bloccano il primo agente per errore.
- Il workspace viene creato senza stato progetto o senza handoff directory.

## Esempio minimo

```markdown
# Project Bootstrap: ceramic-cozy-landing

## Metadata

- project-id: ceramic-cozy-landing
- workspace-path: projects/ceramic-cozy-landing
- source-request: input/initial-request.md

## Created Artifacts

- projects/ceramic-cozy-landing/input/initial-request.md
- projects/ceramic-cozy-landing/blueprints/bootstrap-execution-blueprint.md
- projects/ceramic-cozy-landing/generated-agents/requirement-analyst-agent-package.md
- projects/ceramic-cozy-landing/human-gates/approve-requirements.md

## Next Action

Run Requirement Analyst with `runtime-adapters/codex.md`.
```
