# Runtime Adapter: Claude Code

## Scopo

Tradurre un Agent Package generico in una sessione Claude Code eseguibile, preservando confini, Human Gate, handoff e Knowledge Candidate definiti nel package.

Questo adapter descrive come preparare il contesto di una sessione Claude Code (tramite CLI, IDE extension o web) per eseguire un singolo Agent Package in modo controllato e tracciabile.

## Quando Usarlo

Usare questo adapter quando:

- un Agent Package deve essere eseguito tramite Claude Code CLI (`claude`) o estensione IDE;
- il task richiede accesso diretto al filesystem e al repository git;
- si vuole sfruttare la capacità di Claude Code di leggere, modificare e committare file autonomamente;
- il progetto beneficia di sessioni isolate per agente, con contesto controllato tramite `CLAUDE.md`;
- il workflow richiede integrazione con git (branch, commit, PR).

## Relazione Con Manual Execution

`runtime-adapters/claude-code.md` specializza `runtime-adapters/manual-execution.md`.

Claude Code deve seguire:

1. le regole del Manual Execution Adapter;
2. le regole aggiuntive di questo adapter;
3. l'Agent Package;
4. l'Execution Blueprint;
5. gli standard e le capability indicati dal package.

In caso di conflitto:

1. Human Gate e boundaries prevalgono sempre;
2. Agent Package prevale sulle preferenze runtime;
3. gli standard prevalgono sulle istruzioni libere nel `CLAUDE.md`;
4. runtime hints non possono cambiare scope, strategia o architettura.

## Modello Di Esecuzione

Una sessione Claude Code esegue un solo Agent Package.

```text
Agent Package
+ Execution Blueprint
+ Claude Code Adapter
+ Manual Execution Adapter
+ CLAUDE.md (contesto sessione)
= sessione Claude Code per un singolo agente
```

La sessione produce solo gli output richiesti dal package, più handoff, review evidence o Knowledge Candidate se previsti.

## Input Richiesti

- Percorso repository.
- Percorso Agent Package.
- Percorso Execution Blueprint.
- Project Workspace accessibile da Claude Code.
- Human Gate rilevanti nel Project Workspace.
- Capability, archetype o definizione ad hoc indicati dal package.

## Output Richiesti

- Deliverable indicati dall'Agent Package.
- Handoff conforme a `standards/handoff-standard.md`.
- Eventuali review report richiesti.
- Eventuali Knowledge Candidate conformi a `standards/knowledge-candidate-standard.md`.
- Riepilogo finale con stato, file creati/modificati, verifiche, blocchi e rischi residui.

## Preparazione Del Contesto

### Opzione A — CLAUDE.md di sessione

Creare un file `CLAUDE.md` temporaneo nella radice del repository (o in `projects/<project-id>/`) con il contenuto dell'Agent Package come istruzioni di sessione:

```markdown
# Sessione AgentFactory

Sei un agente temporaneo in esecuzione tramite il Claude Code Runtime Adapter.

## Agent Package

<incollare il contenuto completo del package>

## Adapter attivi

- runtime-adapters/claude-code.md
- runtime-adapters/manual-execution.md

## Regole operative

- Esegui un solo Agent Package in questa sessione.
- Leggi tutti gli input indicati nell'Agent Package prima di modificare file.
- Controlla gli Human Gate nel Project Workspace prima di procedere.
- Se un Human Gate Pending blocca il task corrente, fermati e segnala stato blocked.
- Rispetta boundaries, responsibilities, workflow e Definition of Done del package.
- Non modificare standard permanenti, archetype, capability o agenti permanenti
  salvo istruzione esplicita nell'Agent Package.
- Produci solo gli output richiesti.
- Produci handoff conforme a standards/handoff-standard.md se richiesto.
- Se emerge una lezione riutilizzabile, crea una Knowledge Candidate.
- Alla fine riepiloga stato finale, file creati/modificati, verifiche, blocchi e rischi.
```

### Opzione B — Primo messaggio della sessione

In alternativa al `CLAUDE.md`, iniziare la sessione con un primo messaggio che includa:

```text
Esegui un Agent Package AgentFactory usando il Claude Code Runtime Adapter.

Adapter principale: runtime-adapters/claude-code.md
Adapter base: runtime-adapters/manual-execution.md
Agent Package: <percorso-agent-package>
Execution Blueprint: <percorso-execution-blueprint>
Project Workspace: <percorso-workspace>

[stesse regole operative dell'opzione A]
```

### Preferenza

Preferire l'Opzione A (CLAUDE.md) quando:
- la sessione Claude Code è lunga o multi-step;
- si usano le estensioni IDE dove il contesto CLAUDE.md è caricato automaticamente;
- il package contiene molte regole operative che rischiano di essere dimenticate nel contesto.

Preferire l'Opzione B (primo messaggio) per sessioni brevi o test rapidi.

## Preflight Della Sessione

Prima di modificare file, Claude Code deve:

1. leggere l'Agent Package completo;
2. leggere l'Execution Blueprint;
3. leggere `runtime-adapters/manual-execution.md`;
4. leggere questo adapter;
5. leggere gli standard indicati dal package;
6. leggere le capability assegnate;
7. leggere archetype o definizione ad hoc indicata da `agent-source`;
8. controllare Human Gate nel Project Workspace;
9. controllare lo stato git (`git status`);
10. fermarsi se un input obbligatorio manca o se un Human Gate `Pending` blocca il task.

## Regole Per Human Gate

Claude Code deve fermarsi quando:

- esiste un Human Gate `Pending` il cui `blocking-scope` include il task corrente;
- un gate è `Rejected`, `Expired` o `Changes Requested` e l'Execution Blueprint non indica una strada chiara;
- servirebbe una decisione umana non prevista dal package.

Quando si ferma, Claude Code deve:

- non produrre deliverable parziali come se fossero finali;
- spiegare quale gate blocca e perché;
- indicare il file del gate e la decisione richiesta;
- lasciare stato finale `blocked` nel riepilogo.

Il maintainer umano aggiorna il file Human Gate nel Project Workspace e riprende la sessione o ne avvia una nuova.

## Regole Di Modifica File E Git

Claude Code può modificare solo file necessari agli output dell'Agent Package.

Claude Code non deve:

- modificare standard permanenti, archetype, capability o agenti permanenti salvo esplicito incarico nel package;
- correggere problemi fuori scope notati durante l'esecuzione;
- committare o fare push senza che l'Agent Package lo richieda esplicitamente;
- decidere Human Gate al posto del maintainer umano;
- integrare Knowledge Candidate nella conoscenza permanente.

Se l'Agent Package richiede operazioni git:

- usare branch dedicato per ogni agente o task significativo;
- commit message descrittivi che citano il package-id;
- non fare push senza istruzione esplicita nel package.

## Gestione Del Contesto

Claude Code ha una finestra di contesto limitata. Per sessioni su repository grandi:

- non caricare tutto il repository nel contesto;
- leggere solo i file indicati nell'Agent Package come input;
- usare le capability assegnate come riferimento operativo, non come lettura integrale a inizio sessione;
- caricare standard e capability solo quando necessari al task corrente.

Se il contesto rischia di diventare troppo grande, segnalarlo come rischio nel riepilogo finale.

## Handoff

Il file handoff deve essere creato nel Project Workspace:

```text
projects/<project-id>/handoffs/<sender>-to-<recipient>.md
```

Il contenuto deve essere conforme a `standards/handoff-standard.md`.

## Knowledge Candidate

Claude Code deve creare una Knowledge Candidate quando scopre un miglioramento riutilizzabile, per esempio:

- un Agent Package manca un input necessario per una sessione Claude Code;
- un Human Gate non ha blocking scope chiaro;
- le capability assegnate non coprono un aspetto rilevante del task;
- questo adapter necessita di una nuova regola;
- una sessione Claude Code ha dimostrato un pattern utile per altri progetti.

Il file deve stare in:

```text
projects/<project-id>/knowledge-candidates/
```

## Template Primo Messaggio

```text
Esegui un Agent Package AgentFactory usando il Claude Code Runtime Adapter.

Adapter principale: runtime-adapters/claude-code.md
Adapter base: runtime-adapters/manual-execution.md
Agent Package: {{agent_package_path}}
Execution Blueprint: {{execution_blueprint_path}}
Project Workspace: {{project_workspace_path}}

Regole operative:
- Esegui un solo Agent Package in questa sessione.
- Leggi tutti gli input indicati nell'Agent Package prima di modificare file.
- Controlla gli Human Gate nel Project Workspace prima di procedere.
- Se un Human Gate Pending blocca il task corrente, fermati e segnala stato blocked.
- Rispetta boundaries, responsibilities, workflow e Definition of Done del package.
- Non modificare standard permanenti, archetype, capability o agenti permanenti
  salvo istruzione esplicita nell'Agent Package.
- Produci solo gli output richiesti dall'Agent Package.
- Produci handoff conforme a standards/handoff-standard.md se richiesto.
- Se emerge una lezione riutilizzabile, crea una Knowledge Candidate nel Project Workspace.
- Alla fine riepiloga stato finale, file creati/modificati, verifiche, blocchi e rischi.
```

## Stati Finali

| Stato | Significato |
|---|---|
| `completed` | Output richiesti creati, DoD verificata, handoff prodotto se richiesto. |
| `blocked` | Input mancante, Human Gate bloccante, decisione umana richiesta. |
| `changes-requested` | Review o Human Gate richiede modifiche. |
| `failed` | Task non completabile nel contesto disponibile. |

## Riepilogo Finale Obbligatorio

La risposta finale della sessione Claude Code deve includere:

- stato finale;
- Agent Package eseguito;
- file creati;
- file modificati;
- operazioni git eseguite (se presenti);
- verifiche eseguite;
- Human Gate controllati;
- handoff prodotto;
- Knowledge Candidate prodotte;
- rischi residui;
- prossimo agente o fase consigliata.

## Failure Mode Da Evitare

- Usare una sessione Claude Code per eseguire più Agent Package senza handoff intermedi.
- Saltare Human Gate perché la decisione sembra ovvia.
- Modificare conoscenza permanente mentre si esegue un agente temporaneo.
- Allargare il task oltre i boundaries dell'Agent Package.
- Caricare tutto il repository nel contesto senza necessità.
- Produrre output richiesti ma omettere handoff.
- Fare commit o push senza istruzione esplicita nel package.
- Confondere review approval con Human Gate approval.
- Creare Knowledge Candidate e poi integrarla direttamente senza Knowledge Evolution.

## Criteri Di Completamento Dell'Adapter

Questo adapter è applicato correttamente quando:

1. il contesto della sessione include Agent Package, Execution Blueprint e Project Workspace;
2. Claude Code legge adapter, package, blueprint, capability e standard rilevanti prima di agire;
3. Human Gate sono controllati prima delle modifiche;
4. Claude Code modifica solo file coerenti con l'Agent Package;
5. output e handoff richiesti sono prodotti;
6. eventuali Knowledge Candidate restano nel Project Workspace;
7. la risposta finale dichiara stato, verifiche, operazioni git e rischi.
