# Runtime Adapter: OpenCode

## Scopo

Tradurre un Agent Package generico in una sessione OpenCode eseguibile, preservando confini, Human Gate, handoff e Knowledge Candidate definiti nel package.

OpenCode è un AI coding assistant open source con interfaccia terminale (TUI). Supporta più provider AI (Anthropic, OpenAI, ecc.) e ha accesso diretto al filesystem del progetto. Questo adapter descrive come preparare e condurre una sessione OpenCode per eseguire un singolo Agent Package in modo controllato e tracciabile.

## Quando Usarlo

Usare questo adapter quando:

- si vuole un runtime open source senza dipendenza da strumenti proprietari;
- il team preferisce pieno controllo sul modello AI usato (provider configurabile);
- il task richiede accesso diretto al filesystem e al repository git;
- si lavora in ambienti air-gapped o con vincoli di licenza su tool proprietari;
- si vuole eseguire Agent Package su modelli self-hosted o provider alternativi.

## Relazione Con Manual Execution

`runtime-adapters/opencode.md` specializza `runtime-adapters/manual-execution.md`.

OpenCode deve seguire:

1. le regole del Manual Execution Adapter;
2. le regole aggiuntive di questo adapter;
3. l'Agent Package;
4. l'Execution Blueprint;
5. gli standard e le capability indicati dal package.

In caso di conflitto:

1. Human Gate e boundaries prevalgono sempre;
2. Agent Package prevale sulle preferenze runtime;
3. gli standard prevalgono sul prompt di sessione;
4. runtime hints non possono cambiare scope, strategia o architettura.

## Modello Di Esecuzione

Una sessione OpenCode esegue un solo Agent Package.

```text
Agent Package
+ Execution Blueprint
+ OpenCode Adapter
+ Manual Execution Adapter
= primo messaggio della sessione OpenCode
```

La sessione produce solo gli output richiesti dal package, più handoff, review evidence o Knowledge Candidate se previsti.

## Prerequisiti

1. OpenCode installato (`npm install -g opencode-ai` o metodo equivalente).
2. Provider AI configurato — consigliato Anthropic (`claude-opus-4-8` o `claude-sonnet-4-6`):

```bash
# Configurazione provider Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# Oppure tramite file di configurazione OpenCode
# ~/.config/opencode/config.json
```

3. Repository clonato localmente con workspace del progetto presente.
4. Agent Package valido conforme a `standards/agent-package-standard.md`.
5. Execution Blueprint presente in `projects/<project-id>/blueprints/`.

## Avvio Della Sessione

Aprire il terminale nella radice del repository ed eseguire:

```bash
cd /percorso/del/repository
opencode
```

OpenCode si apre con accesso all'intero filesystem del repository. Ogni sessione esegue un solo Agent Package.

## Primo Messaggio — Template

Copiare e incollare questo template come primo messaggio della sessione, sostituendo le variabili:

```text
Esegui un Agent Package AgentFactory usando il OpenCode Runtime Adapter.

Adapter principale:
runtime-adapters/opencode.md

Adapter base:
runtime-adapters/manual-execution.md

Agent Package da eseguire:
{{agent_package_path}}

Execution Blueprint:
{{execution_blueprint_path}}

Project Workspace:
{{project_workspace_path}}

Regole operative:
- Leggi runtime-adapters/opencode.md e runtime-adapters/manual-execution.md prima di agire.
- Leggi l'Agent Package completo prima di modificare qualsiasi file.
- Leggi le capability assegnate nell'Agent Package.
- Controlla i Human Gate nel Project Workspace prima di iniziare il task.
- Se un Human Gate Pending blocca il task corrente, fermati e segnala stato blocked.
- Rispetta boundaries, responsibilities, workflow e Definition of Done dell'Agent Package.
- Non modificare standard permanenti, archetype, capability o agenti permanenti
  salvo istruzione esplicita nell'Agent Package.
- Produci solo gli output richiesti dall'Agent Package.
- Produci handoff conforme a standards/handoff-standard.md se richiesto.
- Se emerge una lezione riutilizzabile, crea una Knowledge Candidate nel Project Workspace.
- Non integrare Knowledge Candidate nella conoscenza permanente — quella è competenza
  di Knowledge Evolution e richiede approvazione esplicita.
- Alla fine riepiloga: stato finale, file creati/modificati, verifiche eseguite,
  Human Gate controllati, handoff prodotto, rischi residui, prossimo agente consigliato.
```

## Esempio Concreto

```text
Esegui un Agent Package AgentFactory usando il OpenCode Runtime Adapter.

Adapter principale:
runtime-adapters/opencode.md

Adapter base:
runtime-adapters/manual-execution.md

Agent Package da eseguire:
projects/my-api-project/generated-agents/developer-node-api.md

Execution Blueprint:
projects/my-api-project/blueprints/execution-blueprint.md

Project Workspace:
projects/my-api-project

[stesse regole operative del template]
```

## Preflight Obbligatorio

Prima di modificare qualsiasi file, OpenCode deve leggere nell'ordine:

1. `runtime-adapters/opencode.md` (questo file)
2. `runtime-adapters/manual-execution.md`
3. l'Agent Package indicato nel primo messaggio
4. l'Execution Blueprint
5. gli standard citati nel package
6. le capability assegnate nel package
7. l'archetype o definizione ad hoc indicata in `agent-source`
8. i file Human Gate in `projects/<id>/human-gates/` (se presenti)

Se un input obbligatorio manca, fermarsi con stato `blocked`.

## Regole Per Human Gate

OpenCode si ferma quando trova un Human Gate con `status: Pending` il cui `blocking-scope` include il task corrente.

Quando si ferma:

- non produrre output parziali come se fossero finali;
- dichiarare quale gate blocca e perché;
- indicare il file del gate e la decisione richiesta al maintainer umano;
- lasciare stato finale `blocked` nel riepilogo.

Comportamento per stato:

| Stato | Comportamento |
|---|---|
| `Pending` | Fermarsi. Dichiarare il blocco. |
| `Approved` | Proseguire. |
| `Changes Requested` | Tornare alla fase indicata in `return-to-phase`. |
| `Rejected` | Bloccare o chiudere secondo l'Execution Blueprint. |
| `Cancelled` | Ignorare il gate se non esistono altri blocchi. |
| `Expired` | Fermarsi e chiedere nuova decisione o escalation. |

Il maintainer umano aggiorna il file Human Gate nel Project Workspace, poi avvia una nuova sessione OpenCode o riprende il workflow.

## Regole Di Modifica File E Git

OpenCode può modificare solo i file necessari agli output dichiarati nell'Agent Package.

OpenCode non deve:

- modificare standard, archetype, capability o agenti permanenti salvo incarico esplicito;
- correggere problemi fuori scope notati durante l'esecuzione;
- fare commit o push senza istruzione esplicita nell'Agent Package;
- decidere Human Gate al posto del maintainer;
- integrare Knowledge Candidate nella conoscenza permanente.

Se l'Agent Package richiede operazioni git:

- usare un branch dedicato per il task;
- commit message che citano il `package-id`;
- non fare push senza istruzione esplicita.

## Gestione Del Contesto

OpenCode carica il filesystem nella finestra di contesto. Per repository grandi:

- leggere solo i file indicati nell'Agent Package come `inputs`;
- caricare le capability assegnate su richiesta, non tutte a inizio sessione;
- non esplorare directory non indicate nel package.

Se il contesto rischia di saturarsi, segnalarlo nel riepilogo finale come rischio residuo e proporre di suddividere il task in Agent Package più piccoli (Knowledge Candidate per l'Execution Blueprint).

## Handoff

Il file handoff va creato nel Project Workspace:

```text
projects/<project-id>/handoffs/<sender>-to-<recipient>.md
```

Il contenuto deve essere conforme a `standards/handoff-standard.md`.

Dopo aver creato il file, validarlo con:

```bash
python tools/validate.py projects/<project-id>/handoffs/<sender>-to-<recipient>.md
```

## Knowledge Candidate

Creare una Knowledge Candidate in `projects/<project-id>/knowledge-candidates/` quando:

- una pratica emersa sembra riutilizzabile oltre questo progetto;
- un agente ad hoc potrebbe diventare archetype;
- una capability è insufficiente o mancante;
- questo adapter necessita di una nuova regola;
- una sessione OpenCode ha mostrato un pattern utile per altri progetti.

Non integrare direttamente — produrre il file e lasciare che Knowledge Evolution valuti.

## Stati Finali

| Stato | Significato |
|---|---|
| `completed` | Output richiesti prodotti, DoD verificata, handoff prodotto se richiesto. |
| `blocked` | Input mancante, Human Gate Pending, decisione umana richiesta. |
| `changes-requested` | Review o Human Gate richiede modifiche. |
| `failed` | Task non completabile nel contesto disponibile. |

## Riepilogo Finale Obbligatorio

La risposta finale della sessione OpenCode deve includere:

- stato finale (`completed` / `blocked` / `changes-requested` / `failed`);
- Agent Package eseguito;
- file creati;
- file modificati;
- operazioni git eseguite (se presenti);
- verifiche eseguite e loro esito;
- Human Gate controllati;
- handoff prodotto (percorso file);
- Knowledge Candidate prodotte;
- rischi residui;
- prossimo agente o fase consigliata.

## Differenze Rispetto A Claude Code

| Aspetto | OpenCode | Claude Code |
|---|---|---|
| Contesto sessione | Primo messaggio (no file di config equivalente a CLAUDE.md) | CLAUDE.md o primo messaggio |
| Provider AI | Configurabile (Anthropic, OpenAI, ecc.) | Solo Anthropic |
| Open source | Sì | No |
| Costo | Dipende dal provider scelto | Abbonamento Anthropic |
| Integrazione IDE | TUI terminale | CLI + estensioni IDE |
| Self-hosting | Possibile con modelli compatibili | No |

## Failure Mode Da Evitare

- Usare una sessione OpenCode per eseguire più Agent Package senza handoff intermedi.
- Saltare il preflight e la lettura dei file indicati nel package.
- Modificare conoscenza permanente durante l'esecuzione di un agente temporaneo.
- Allargare il task oltre i boundaries del package.
- Non produrre il handoff al termine del task.
- Fare commit o push senza istruzione esplicita nel package.
- Creare Knowledge Candidate e integrarla direttamente senza Knowledge Evolution.
- Confondere review approval con Human Gate approval.

## Criteri Di Completamento Dell'Adapter

Questo adapter è applicato correttamente quando:

1. il primo messaggio include Agent Package, Execution Blueprint e Project Workspace;
2. OpenCode legge adapter, package, blueprint, capability e standard prima di agire;
3. i Human Gate sono controllati prima delle modifiche;
4. OpenCode modifica solo i file coerenti con l'Agent Package;
5. output e handoff richiesti sono prodotti;
6. le Knowledge Candidate restano nel Project Workspace;
7. il riepilogo finale dichiara stato, verifiche, git operations e rischi.
