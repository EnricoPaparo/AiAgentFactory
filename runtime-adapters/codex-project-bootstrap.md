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

## Output Richiesti

- Project Workspace iniziale in `projects/<project-id>/`.
- `input/initial-request.md`.
- `project-status.md`.
- `blueprints/bootstrap-execution-blueprint.md`.
- `generated-agents/requirement-analyst-agent-package.md`.
- eventuale `human-gates/approve-requirements.md`.
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
- Crea blueprints/bootstrap-execution-blueprint.md solo per avviare Requirement Analyst.
- Crea generated-agents/requirement-analyst-agent-package.md.
- Crea human-gates/approve-requirements.md se serve validare i requisiti prima della soluzione.
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
Voglio un minimale e semplicissimo sito web moderno in stile cozy che riguarda la ceramica.
Basta una landing page e una pagina contatti inventata lasciando vuoti i veri contatti.

Regole:
- Crea un solo Project Workspace sotto projects/<project-id>/.
- Preserva la richiesta originale in input/initial-request.md.
- Crea project-status.md.
- Crea blueprints/bootstrap-execution-blueprint.md solo per avviare Requirement Analyst.
- Crea generated-agents/requirement-analyst-agent-package.md.
- Crea human-gates/approve-requirements.md se serve validare i requisiti prima della soluzione.
- Non produrre Requirements Blueprint.
- Non scegliere stack, architettura o design tecnico.
- Non implementare deliverable.
- Alla fine restituisci il prompt pronto per eseguire Requirement Analyst con runtime-adapters/codex.md.
```

## Criteri Di Completamento

Il bootstrap Codex e completato quando:

1. il workspace esiste;
2. la richiesta originale e salvata;
3. il primo Agent Package e pronto;
4. il primo Human Gate non blocca Requirement Analyst;
5. il prompt successivo e pronto;
6. non sono stati prodotti blueprint successivi o deliverable.
