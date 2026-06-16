# Runtime Adapter: Codex Project Bootstrap

## Scopo

Avviare un nuovo progetto AgentFactory da una richiesta utente grezza usando Codex come esecutore del Factory Intake.

Questo adapter prepara il primo Project Workspace e il primo Agent Package. Non esegue l'intera pipeline.

## Quando Usarlo

Usare questo adapter quando l'utente vuole dare alla factory una nuova idea di progetto senza creare manualmente cartelle, blueprint o Agent Package iniziali.

## Input Richiesti

- Richiesta utente originale.
- Percorso repository.
- `agents/factory-intake/factory-intake.md`.
- `standards/project-bootstrap-standard.md`.
- `projects/_template/`, se disponibile.
- `runtime-adapters/codex.md`.
- `standards/factory-state-standard.md`.

## Output Richiesti

- Project Workspace iniziale in `projects/<project-id>/`.
- `input/initial-request.md`.
- `project-status.md`.
- `factory-state.json`.
- `artifact-index.md`.
- `blueprints/bootstrap-execution-blueprint.md`.
- `generated-agents/requirement-analyst-agent-package.md`.
- `human-gates/approve-requirements.md`.
- prompt pronto per eseguire il Requirement Analyst.

## Regole

- Preservare la richiesta originale.
- Non produrre Requirements Blueprint.
- Non scegliere stack o architettura.
- Non creare Agent Package oltre al Requirement Analyst.
- Non implementare deliverable.
- Non decidere Human Gate.
- Usare kebab-case per `project-id`.

## Prompt Template

```text
Avvia un nuovo progetto AgentFactory usando Factory Intake.

Repository:
<absolute-repository-path>

Runtime adapter bootstrap:
runtime-adapters/codex-project-bootstrap.md

Factory Intake:
agents/factory-intake/factory-intake.md

Project Bootstrap Standard:
standards/project-bootstrap-standard.md

Richiesta utente originale:
<paste user project idea here>

Regole:
- Crea un solo Project Workspace sotto projects/<project-id>/.
- Preserva la richiesta originale in input/initial-request.md.
- Crea project-status.md.
- Crea factory-state.json con phase requirements e next_action run_requirement_analyst.
- Crea artifact-index.md con gli artefatti iniziali.
- Crea blueprints/bootstrap-execution-blueprint.md solo per avviare Requirement Analyst.
- Crea generated-agents/requirement-analyst-agent-package.md.
- Crea human-gates/approve-requirements.md per validare i requisiti prima della soluzione.
- Registra in project-status.md i gate attesi del pilot: approve-requirements, approve-solution-blueprint, approve-execution-plan, approve-final-delivery.
- Non produrre Requirements Blueprint.
- Non scegliere stack, architettura o design tecnico.
- Non implementare deliverable.
- Alla fine restituisci il prompt pronto per eseguire Requirement Analyst con runtime-adapters/codex.md.
```

## Esempio Reale

```text
Avvia un nuovo progetto AgentFactory usando Factory Intake.

Repository:
C:\Users\Erry\Documents\AiAgentsFactory

Runtime adapter bootstrap:
runtime-adapters/codex-project-bootstrap.md

Factory Intake:
agents/factory-intake/factory-intake.md

Project Bootstrap Standard:
standards/project-bootstrap-standard.md

Richiesta utente originale:
Voglio un minimale e semplicissimo sito web moderno per una piccola attivita artigianale.
Basta una landing page e una pagina contatti lasciando vuoti i veri contatti.

Regole:
- Crea un solo Project Workspace sotto projects/<project-id>/.
- Preserva la richiesta originale in input/initial-request.md.
- Crea project-status.md.
- Crea factory-state.json con phase requirements e next_action run_requirement_analyst.
- Crea artifact-index.md con gli artefatti iniziali.
- Crea blueprints/bootstrap-execution-blueprint.md solo per avviare Requirement Analyst.
- Crea generated-agents/requirement-analyst-agent-package.md.
- Crea human-gates/approve-requirements.md per validare i requisiti prima della soluzione.
- Registra in project-status.md i gate attesi del pilot: approve-requirements, approve-solution-blueprint, approve-execution-plan, approve-final-delivery.
- Non produrre Requirements Blueprint.
- Non scegliere stack, architettura o design tecnico.
- Non implementare deliverable.
- Alla fine restituisci il prompt pronto per eseguire Requirement Analyst con runtime-adapters/codex.md.
```

## Criteri Di Completamento

Il bootstrap Codex e completato quando:

1. il workspace esiste;
2. la richiesta originale e salvata;
3. `factory-state.json` e `artifact-index.md` esistono;
4. il primo Agent Package e pronto;
5. il primo Human Gate non blocca Requirement Analyst;
6. il prompt successivo e pronto;
7. non sono stati prodotti blueprint successivi o deliverable.
