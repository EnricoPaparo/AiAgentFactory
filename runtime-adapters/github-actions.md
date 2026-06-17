# Runtime Adapter: GitHub Actions

## Scopo

Tradurre un Agent Package e un Execution Blueprint in un workflow GitHub Actions eseguibile in CI/CD, preservando confini, Human Gate, handoff e Knowledge Candidate definiti nel package.

Questo adapter descrive come mappare la struttura AgentFactory su job, step, artifact, environment approval e workflow dispatch di GitHub Actions.

## Quando Usarlo

Usare questo adapter quando:

- il progetto è ospitato su GitHub e il team usa già GitHub Actions;
- il workflow deve essere eseguito automaticamente su eventi git (push, PR, schedule);
- si vuole sfruttare i Human Gate tramite GitHub Environments con approvazione obbligatoria;
- gli handoff tra agenti devono essere tracciati come artifact versionati;
- serve un audit trail CI/CD per ogni esecuzione di agente.

## Relazione Con Manual Execution

`runtime-adapters/github-actions.md` estende `runtime-adapters/manual-execution.md`.

Le regole del Manual Execution Adapter rimangono valide. Questo adapter aggiunge le regole di traduzione specifiche per GitHub Actions.

In caso di conflitto:

1. Human Gate e boundaries prevalgono sempre, anche su logica di trigger automatico;
2. Agent Package prevale sulle preferenze di configurazione CI;
3. gli standard prevalgono sulle convenzioni YAML quando ci sono ambiguità.

## Modello Di Esecuzione

```text
Execution Blueprint
  → un job GitHub Actions per ogni Agent Package
  → dipendenze tra job tramite needs:
  → artifact per handoff tra job
  → GitHub Environment per Human Gate bloccanti
  → workflow_dispatch per avvio manuale
```

## Traduzione Agent Package → Job GitHub Actions

### Struttura Base Del Job

```yaml
jobs:
  <agent-role-kebab>:                          # da agent-role nel package
    name: "<agent-role>"
    runs-on: ubuntu-latest
    needs: [<job-precedente>]                  # da workflow Execution Blueprint
    # environment: <human-gate-env>            # solo se Human Gate blocca questo job

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Download handoff da agente precedente
        uses: actions/download-artifact@v4
        with:
          name: handoff-<sender>-to-<recipient>
          path: projects/<project-id>/handoffs/

      - name: Setup runtime
        # installare Python, Node, o altro in base alle capability assegnate
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Esegui Agent Package
        env:
          AGENT_PACKAGE_PATH: projects/<project-id>/generated-agents/<package>.md
          EXECUTION_BLUEPRINT_PATH: projects/<project-id>/blueprints/execution-blueprint.md
          PROJECT_WORKSPACE: projects/<project-id>
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/run_agent.py \
            --package "$AGENT_PACKAGE_PATH" \
            --blueprint "$EXECUTION_BLUEPRINT_PATH" \
            --workspace "$PROJECT_WORKSPACE"

      - name: Verifica Definition of Done
        run: |
          python scripts/verify_dod.py \
            --package "$AGENT_PACKAGE_PATH" \
            --workspace "$PROJECT_WORKSPACE"

      - name: Upload handoff prodotto
        uses: actions/upload-artifact@v4
        with:
          name: handoff-<this-agent>-to-<next-agent>
          path: projects/<project-id>/handoffs/<this>-to-<next>.md
          if-no-files-found: error              # handoff obbligatorio

      - name: Upload deliverable
        uses: actions/upload-artifact@v4
        with:
          name: deliverables-<project-id>
          path: projects/<project-id>/deliverables/
```

## Traduzione Handoff → Artifact

Ogni handoff tra agenti diventa un coppia upload/download di artifact:

```yaml
# Agente mittente (es. Developer)
- name: Upload handoff developer-to-reviewer
  uses: actions/upload-artifact@v4
  with:
    name: handoff-developer-to-reviewer
    path: projects/<id>/handoffs/developer-to-reviewer.md
    if-no-files-found: error    # fallisce se handoff non prodotto

# Agente destinatario (es. Reviewer)
- name: Download handoff developer-to-reviewer
  uses: actions/download-artifact@v4
  with:
    name: handoff-developer-to-reviewer
    path: projects/<id>/handoffs/
```

Il file handoff deve essere conforme a `standards/handoff-standard.md`. La validazione del formato può essere aggiunta come step separato.

## Traduzione Human Gate → GitHub Environment

I Human Gate bloccanti si implementano tramite GitHub Environments con `required reviewers`.

### Configurazione Environment Su GitHub

1. Andare in `Settings → Environments → New environment`.
2. Creare un environment con nome descrittivo: `human-gate-<gate-id>`.
3. Aggiungere `Required reviewers` (le persone autorizzate ad approvare).
4. Opzionalmente impostare `Wait timer` per gate con scadenza.

### Uso Nel Workflow

```yaml
jobs:
  # Job che attende approvazione umana prima di proseguire
  <agent-dopo-gate>:
    name: "<Agente che richiede approvazione>"
    runs-on: ubuntu-latest
    needs: [<agente-precedente>]
    environment: human-gate-<gate-id>          # BLOCCA qui fino ad approvazione
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      # ... resto del job
```

### File Human Gate Aggiornato Da CI

Aggiungere uno step che aggiorna il file Human Gate nel repository dopo l'approvazione:

```yaml
      - name: Aggiorna stato Human Gate
        run: |
          sed -i 's/status: Pending/status: Approved/' \
            projects/<id>/human-gates/<gate-id>.md
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add projects/<id>/human-gates/<gate-id>.md
          git commit -m "Human Gate <gate-id>: Approved via GitHub Environment"
          git push
```

### Comportamento Per Stato Gate

| Stato Environment | Comportamento workflow |
|---|---|
| In attesa di review | Job bloccato — workflow sospeso |
| Approvato | Job procede |
| Rifiutato | Job non si avvia — workflow fallisce |
| Timer scaduto | Job non si avvia — workflow fallisce |

## Workflow Completo Di Esempio

```yaml
# .github/workflows/factory-pipeline.yml

name: AgentFactory Pipeline

on:
  workflow_dispatch:
    inputs:
      project_id:
        description: 'ID del progetto (es. my-project)'
        required: true
      starting_agent:
        description: 'Agent Package di partenza'
        required: true

jobs:
  requirement-analyst:
    name: "Requirement Analyst"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Esegui Requirement Analyst
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python scripts/run_agent.py --package agents/requirement-analyst/requirement-analyst.md
      - uses: actions/upload-artifact@v4
        with:
          name: requirements-blueprint
          path: projects/${{ inputs.project_id }}/blueprints/requirements-blueprint.md
          if-no-files-found: error

  approve-requirements:
    name: "Human Gate: Approva Requirements Blueprint"
    runs-on: ubuntu-latest
    needs: [requirement-analyst]
    environment: human-gate-approve-requirements    # blocca qui
    steps:
      - run: echo "Requirements Blueprint approvato."

  architect:
    name: "Architect"
    runs-on: ubuntu-latest
    needs: [approve-requirements]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: requirements-blueprint
          path: projects/${{ inputs.project_id }}/blueprints/
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Esegui Architect
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python scripts/run_agent.py --package agents/architect/architect.md
      - uses: actions/upload-artifact@v4
        with:
          name: solution-blueprint
          path: projects/${{ inputs.project_id }}/blueprints/solution-blueprint.md
          if-no-files-found: error

  developer:
    name: "Developer"
    runs-on: ubuntu-latest
    needs: [architect]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: solution-blueprint
          path: projects/${{ inputs.project_id }}/blueprints/
      - name: Esegui Developer Agent
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python scripts/run_agent.py --package ${{ inputs.starting_agent }}
      - uses: actions/upload-artifact@v4
        with:
          name: handoff-developer-to-reviewer
          path: projects/${{ inputs.project_id }}/handoffs/developer-to-reviewer.md
          if-no-files-found: error

  reviewer:
    name: "Reviewer"
    runs-on: ubuntu-latest
    needs: [developer]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: handoff-developer-to-reviewer
          path: projects/${{ inputs.project_id }}/handoffs/
      - name: Esegui Reviewer Agent
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python scripts/run_agent.py --package projects/${{ inputs.project_id }}/generated-agents/reviewer.md
      - uses: actions/upload-artifact@v4
        with:
          name: review-report
          path: projects/${{ inputs.project_id }}/reviews/
          if-no-files-found: error

  pipeline-supervisor:
    name: "Pipeline Supervisor"
    runs-on: ubuntu-latest
    needs: [reviewer]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: review-report
          path: projects/${{ inputs.project_id }}/reviews/
      - name: Verifica processo
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python scripts/run_agent.py --package agents/pipeline-supervisor/pipeline-supervisor.md
```

## Validazione Handoff Come Step Separato

Aggiungere un step di validazione prima di ogni upload per garantire conformità allo standard:

```yaml
      - name: Valida handoff
        run: |
          python scripts/validate_artifact.py \
            --artifact projects/<id>/handoffs/<sender>-to-<recipient>.md \
            --standard standards/handoff-standard.md
```

Il file `scripts/validate_artifact.py` è parte del tooling della factory (vedi Fase 4 del piano di sviluppo).

## Secrets E Variabili D'Ambiente

| Secret/Variabile | Scopo | Dove configurare |
|---|---|---|
| `OPENAI_API_KEY` | Chiave API per agenti LLM | Repository → Settings → Secrets |
| `ANTHROPIC_API_KEY` | Chiave API per agenti Claude | Repository → Settings → Secrets |
| `PROJECT_ID` | ID progetto corrente | Input del workflow_dispatch |
| `AGENT_PACKAGE_PATH` | Percorso Agent Package | Env del job |

Non inserire mai chiavi API o segreti nei file YAML del workflow. Usare sempre `${{ secrets.SECRET_NAME }}`.

## Trigger Consigliati

| Trigger | Uso |
|---|---|
| `workflow_dispatch` | Avvio manuale di una pipeline factory su un progetto |
| `push` (su branch specifico) | Avvio automatico dopo merge di blueprint |
| `schedule` | Esecuzione periodica di task ricorrenti (es. security audit) |
| `pull_request` | Review automatica su ogni PR (es. reviewer agent) |

## Failure Mode Da Evitare

- Usare un singolo job per eseguire più Agent Package — un job per package.
- Saltare l'upload di artifact handoff: il job successivo non può verificare cosa è stato prodotto.
- Configurare un Environment GitHub senza required reviewers — il Human Gate diventa un no-op.
- Usare `continue-on-error: true` su step critici come la verifica della Definition of Done.
- Committare conoscenza permanente direttamente da un job CI senza passare per Knowledge Evolution.
- Usare variabili d'ambiente per passare segreti in chiaro nei log.
- Condividere stato tra agenti tramite variabili d'ambiente invece di artifact — le variabili non sono tracciate.

## Criteri Di Completamento Dell'Adapter

Questo adapter è applicato correttamente quando:

1. ogni Agent Package corrisponde a un job distinto nel workflow;
2. i job sono collegati tramite `needs:` secondo il workflow dell'Execution Blueprint;
3. ogni handoff è un artifact caricato dal job mittente e scaricato dal job destinatario;
4. ogni Human Gate è implementato come GitHub Environment con required reviewers;
5. i segreti sono gestiti tramite GitHub Secrets, mai in chiaro nel YAML;
6. la Definition of Done è verificata come step prima dell'upload degli output finali;
7. le Knowledge Candidate sono salvate nel Project Workspace, non integrate direttamente.
