# Runtime Adapter: Codex Conversation

## Scopo

Eseguire AgentFactory in una singola conversazione Codex, coordinando piu fasi e piu Agent Package senza richiedere all'utente di aprire una nuova chat per ogni agente.

Questo adapter usa `agents/factory-host/factory-host.md` come coordinatore conversazionale.

Quando disponibile, usa `agents/factory-runner/factory-runner.md` e `factory-state.json` per evitare di ricostruire lo stato leggendo tutti gli artefatti.

## Quando Usarlo

Usare questo adapter quando l'utente vuole:

- dare un'idea di progetto e lasciare che la factory proceda;
- ricevere documenti e Human Gate nella stessa chat;
- approvare o respingere gate senza copiare prompt tra sessioni;
- far generare ed eseguire agenti temporanei in sequenza.

## Modello

```text
User idea
-> Factory Host
-> Factory Runner
-> Factory Intake
-> Requirement Analyst
-> Human Gate: approve-requirements
-> Architect
-> Human Gate: approve-solution-blueprint
-> Pipeline Designer
-> Human Gate: approve-execution-plan
-> Knowledge Compiler
-> Agent Packages
-> Runtime Packets
-> Runtime Adapter per Agent Package
-> Reviewer
-> Pipeline Supervisor
-> Human Gate: approve-final-delivery
-> Knowledge Evolution
```

## Regola Principale

Codex non deve chiedere all'utente di incollare prompt per ogni agente. Deve mantenere la conversazione, produrre gli artefatti, fermarsi sui gate e proseguire dopo decisione esplicita.

## Input Richiesti

- Richiesta utente o Project Workspace.
- `agents/factory-host/factory-host.md`.
- `runtime-adapters/codex-conversation.md`.
- `runtime-adapters/codex.md`.
- `runtime-adapters/manual-execution.md`.
- `agents/factory-runner/factory-runner.md`, quando presente.
- Standard e agenti permanenti necessari alla fase corrente.

## Stato Conversazionale

Factory Host deve mantenere e aggiornare:

- project-id;
- fase corrente;
- artefatto corrente;
- agente corrente;
- gate aperti;
- prossimo passo;
- rischi o blocchi.

Lo stato persistente vive in:

```text
projects/<project-id>/project-status.md
projects/<project-id>/factory-state.json
```

`project-status.md` serve all'umano. `factory-state.json` serve al runtime.

## Human Gate Inline

Quando serve approvazione, Codex deve fermarsi e chiedere:

```text
Human Gate: <gate-id>
Decisione richiesta: <decision-required>
Blocking scope: <blocking-scope>
Opzioni: Approved / Changes Requested / Rejected

Rispondi con una delle opzioni e note eventuali.
```

Finche l'utente non decide, Codex non deve proseguire con task downstream.

## Esecuzione Degli Agenti

Per agenti permanenti:

- usare il file in `agents/<agent>/`;
- produrre l'artefatto previsto dallo standard;
- produrre handoff quando la fase passa ad altro ruolo.

Per agenti temporanei:

- leggere prima il runtime packet in `runtime-packets/`, se presente;
- usare l'Agent Package generato in `generated-agents/`;
- applicare `runtime-adapters/codex.md`;
- produrre output e handoff richiesti.

## Prompt Di Avvio Breve

Questo e il prompt preferito quando il repository contiene Factory Runner:

```text
Esegui AgentFactory su questa idea:
<paste project idea here>

Repository:
<absolute-repository-path>

Regole:
- Usa Factory Host, Factory Runner e Codex Conversation Adapter.
- Mantieni tutto nella stessa chat.
- Crea o aggiorna factory-state.json.
- Fermati sui gate: requisiti, architettura, piano/team agenti, lavoro finito.
- Usa summaries e runtime packet per ridurre il contesto degli agenti temporanei.
- Usa tools/factory.py per validazioni, next action, packet display e approval bookkeeping quando possibile.
```

## Prompt Di Avvio

```text
Esegui AgentFactory in modalita conversazionale usando Codex Conversation Adapter.

Repository:
<absolute-repository-path>

Factory Host:
agents/factory-host/factory-host.md

Factory Runner:
agents/factory-runner/factory-runner.md

Conversation adapter:
runtime-adapters/codex-conversation.md

Single-agent adapter:
runtime-adapters/codex.md

Manual adapter base:
runtime-adapters/manual-execution.md

Richiesta utente:
<paste project idea here>

Regole:
- Mantieni tutto nella stessa chat.
- Crea o aggiorna factory-state.json.
- Se non esiste un Project Workspace, avvia Factory Intake.
- Produci gli artefatti fase per fase.
- Usa tools/factory.py validate quando esiste factory-state.json.
- Dopo ogni Human Gate Pending, fermati e chiedi Approved / Changes Requested / Rejected.
- Dopo approval, prosegui con la fase successiva.
- Per un pilot end-to-end usa almeno questi gate: approve-requirements, approve-solution-blueprint, approve-execution-plan, approve-final-delivery.
- Non saltare Requirement Analyst, Architect, Pipeline Designer o Knowledge Compiler quando richiesti.
- Crea ed esegui Agent Package temporanei quando il progetto arriva alla fase operativa.
- Genera runtime packet e usali prima di passare contesto completo agli agenti temporanei.
- Ogni fase deve scrivere file nel Project Workspace.
- Alla fine di ogni fase, riepiloga file creati/modificati e prossimo passo.
```

## Prompt Di Ripresa

Usare quando un progetto esiste gia.

```text
Riprendi AgentFactory in modalita conversazionale.

Repository:
<absolute-repository-path>

Project Workspace:
projects/<project-id>

Factory Host:
agents/factory-host/factory-host.md

Factory Runner:
agents/factory-runner/factory-runner.md

Conversation adapter:
runtime-adapters/codex-conversation.md

Regole:
- Leggi prima factory-state.json, se esiste.
- Usa project-status.md come stato leggibile per l'umano.
- Identifica fase corrente, gate aperti e prossimo passo tramite Factory Runner.
- Se un Human Gate e Pending, chiedi decisione.
- Altrimenti prosegui con la fase successiva prevista.
- Usa summaries e runtime packet prima di rileggere blueprint completi.
```

## Criteri Di Completamento

Questo adapter e applicato correttamente quando:

1. l'utente puo dare una sola richiesta iniziale;
2. Codex crea o riprende il Project Workspace;
3. Codex crea o aggiorna `factory-state.json`;
4. Codex produce artefatti fase per fase;
5. Codex chiede approval inline sui Human Gate;
6. Codex applica i gate minimi: requisiti, architettura, piano/team agenti, lavoro finito;
7. Codex prosegue dopo approvazione senza richiedere nuovo prompt agente;
8. gli Agent Package temporanei vengono generati e usati;
9. i runtime packet comprimono il contesto operativo;
10. le azioni deterministiche sono registrate in run-records;
11. il progetto mantiene stato persistente nel workspace.

## Failure Mode Da Evitare

- Chiedere all'utente di aprire una nuova chat per ogni agente.
- Proseguire oltre un Human Gate Pending.
- Combinare tutte le fasi in un solo documento non verificabile.
- Eseguire task tecnici senza Agent Package.
- Non aggiornare `project-status.md`.
- Non aggiornare `factory-state.json`.
- Perdere handoff tra agenti.
