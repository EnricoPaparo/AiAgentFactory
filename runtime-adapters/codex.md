# Runtime Adapter: Codex

## Scopo

Tradurre un Agent Package generico in una sessione operativa Codex eseguibile in modo ripetibile, preservando confini, Human Gate, handoff e Knowledge Candidate.

Questo adapter non e un orchestratore automatico. Definisce come preparare, avviare, guidare e verificare una chat Codex che esegue un singolo Agent Package.

## Quando Usarlo

Usare questo adapter quando:

- un Agent Package deve essere eseguito da Codex;
- serve un prompt standard da incollare in una nuova chat Codex;
- si vuole mantenere separato ogni agente temporaneo in una sessione distinta;
- il progetto richiede handoff verificabili tra agenti o fasi.

## Relazione Con Manual Execution

`runtime-adapters/codex.md` specializza `runtime-adapters/manual-execution.md`.

Codex deve seguire:

1. le regole del Manual Execution Adapter;
2. le regole aggiuntive di questo Codex Adapter;
3. l'Agent Package;
4. l'Execution Blueprint;
5. gli standard e le capability indicati dal package.

In caso di conflitto:

1. Human Gate e boundaries prevalgono sempre;
2. Agent Package prevale sulle preferenze runtime;
3. gli standard prevalgono sulle istruzioni libere del prompt;
4. runtime hints non possono cambiare scope, strategia o architettura.

## Modello Di Esecuzione

Una sessione Codex esegue un solo Agent Package.

```text
Agent Package
+ Execution Blueprint
+ Codex Adapter
+ Manual Execution Adapter
= prompt Codex per una sessione agente
```

La sessione Codex deve produrre solo gli output richiesti dal package, piu handoff, review evidence o Knowledge Candidate se richiesti.

## Input Richiesti

- Percorso repository.
- Percorso Agent Package.
- Percorso Execution Blueprint.
- Percorso `runtime-adapters/codex.md`.
- Percorso `runtime-adapters/manual-execution.md`.
- Project Workspace.
- Human Gate rilevanti.
- Capability, archetype o definizione ad hoc indicati dal package.

## Output Richiesti

- Deliverable indicati dall'Agent Package.
- Handoff conforme a `standards/handoff-standard.md`.
- Eventuali review report richiesti.
- Eventuali Knowledge Candidate conformi a `standards/knowledge-candidate-standard.md`.
- Riepilogo finale con stato, file creati/modificati, verifiche, blocchi e rischi residui.

## Preflight Della Sessione Codex

Prima di modificare file, Codex deve:

1. leggere l'Agent Package;
2. leggere l'Execution Blueprint;
3. leggere `runtime-adapters/manual-execution.md`;
4. leggere questo adapter;
5. leggere gli standard indicati dal package;
6. leggere capability assegnate;
7. leggere archetype o definizione ad hoc indicata da `agent-source`;
8. controllare Human Gate nel Project Workspace;
9. controllare `git status`;
10. fermarsi se un input obbligatorio manca o se un Human Gate `Pending` blocca il task.

## Regole Per Human Gate

Codex deve fermarsi quando:

- esiste un Human Gate `Pending` il cui `blocking-scope` include il task corrente;
- un gate e `Rejected`, `Expired` o `Changes Requested` e l'Execution Blueprint non indica una strada chiara;
- servirebbe una decisione umana non prevista dal package.

Quando si ferma, Codex deve:

- non produrre deliverable parziali come se fossero finali;
- spiegare quale gate blocca;
- indicare file del gate e decisione richiesta;
- lasciare stato finale `blocked`.

## Regole Di Modifica File

Codex puo modificare solo file necessari agli output dell'Agent Package.

Codex non deve:

- modificare standard permanenti, archetype, capability o agenti permanenti salvo esplicito incarico nel package;
- correggere problemi fuori scope;
- chiudere un progetto se il package non e responsabile della closure;
- decidere Human Gate al posto del maintainer umano;
- integrare Knowledge Candidate nella conoscenza permanente.

## Prompt Template

Usare questo template per avviare una nuova chat Codex.

```text
Esegui un Agent Package AgentFactory usando il Codex Runtime Adapter.

Repository:
<absolute-repository-path>

Runtime adapter principale:
runtime-adapters/codex.md

Runtime adapter base:
runtime-adapters/manual-execution.md

Agent Package da eseguire:
<agent-package-path>

Execution Blueprint:
<execution-blueprint-path>

Regole operative:
- Esegui un solo Agent Package in questa chat.
- Segui prima runtime-adapters/codex.md e runtime-adapters/manual-execution.md.
- Leggi tutti gli input indicati nell'Agent Package prima di modificare file.
- Controlla gli Human Gate nel Project Workspace prima di procedere.
- Se un Human Gate Pending blocca il task corrente, fermati e segnala stato blocked.
- Rispetta boundaries, responsibilities, workflow e Definition of Done dell'Agent Package.
- Non modificare standard permanenti, archetype, capability o agenti permanenti salvo istruzione esplicita nell'Agent Package.
- Produci solo gli output richiesti dall'Agent Package.
- Produci handoff conforme a standards/handoff-standard.md se richiesto.
- Se emerge una lezione riutilizzabile, crea una Knowledge Candidate invece di integrare direttamente la conoscenza permanente.
- Alla fine riepiloga stato finale, file creati/modificati, verifiche eseguite, blocchi e rischi residui.
```

## Prompt Template Con Variabili

```text
Esegui un Agent Package AgentFactory usando il Codex Runtime Adapter.

Repository:
{{repository_path}}

Runtime adapter principale:
runtime-adapters/codex.md

Runtime adapter base:
runtime-adapters/manual-execution.md

Agent Package da eseguire:
{{agent_package_path}}

Execution Blueprint:
{{execution_blueprint_path}}

Project Workspace:
{{project_workspace_path}}

Regole operative:
- Esegui un solo Agent Package in questa chat.
- Segui prima runtime-adapters/codex.md e runtime-adapters/manual-execution.md.
- Leggi tutti gli input indicati nell'Agent Package prima di modificare file.
- Controlla gli Human Gate nel Project Workspace prima di procedere.
- Se un Human Gate Pending blocca il task corrente, fermati e segnala stato blocked.
- Rispetta boundaries, responsibilities, workflow e Definition of Done dell'Agent Package.
- Non modificare standard permanenti, archetype, capability o agenti permanenti salvo istruzione esplicita nell'Agent Package.
- Produci solo gli output richiesti dall'Agent Package.
- Produci handoff conforme a standards/handoff-standard.md se richiesto.
- Se emerge una lezione riutilizzabile, crea una Knowledge Candidate invece di integrare direttamente la conoscenza permanente.
- Alla fine riepiloga stato finale, file creati/modificati, verifiche eseguite, blocchi e rischi residui.
```

## Regole Di Stato Finale

Codex deve chiudere la sessione con uno di questi stati:

| Stato | Uso |
|---|---|
| `completed` | Output richiesti creati, DoD verificata, handoff prodotto se richiesto. |
| `blocked` | Input mancante, Human Gate bloccante, decisione umana richiesta o conflitto non risolvibile. |
| `changes-requested` | Review o Human Gate richiede modifiche. |
| `failed` | Task non completabile nel contesto disponibile. |

## Riepilogo Finale Obbligatorio

La risposta finale della sessione Codex deve includere:

- stato finale;
- Agent Package eseguito;
- file creati;
- file modificati;
- verifiche eseguite;
- Human Gate controllati;
- handoff prodotto;
- Knowledge Candidate prodotte;
- rischi residui;
- prossimo agente o fase consigliata.

## Handoff

Se il package richiede handoff, Codex deve creare un file nel Project Workspace, normalmente:

```text
projects/<project-id>/handoffs/<sender>-to-<recipient>.md
```

Il contenuto deve essere conforme a `standards/handoff-standard.md`.

## Knowledge Candidate

Codex deve creare una Knowledge Candidate quando scopre un miglioramento riutilizzabile, per esempio:

- un Agent Package manca un input necessario;
- un Human Gate non ha blocking scope chiaro;
- un archetype e troppo generico;
- una capability manca di checklist utile;
- questo adapter necessita di una nuova regola.

Il file deve stare in:

```text
projects/<project-id>/knowledge-candidates/
```

## Esempio Di Prompt Reale

```text
Esegui un Agent Package AgentFactory usando il Codex Runtime Adapter.

Repository:
C:\Users\Erry\Documents\AiAgentsFactory

Runtime adapter principale:
runtime-adapters/codex.md

Runtime adapter base:
runtime-adapters/manual-execution.md

Agent Package da eseguire:
projects/pilot-agent-package-validation/generated-agents/reviewer-agent-package.md

Execution Blueprint:
projects/pilot-agent-package-validation/blueprints/execution-blueprint.md

Project Workspace:
projects/pilot-agent-package-validation

Regole operative:
- Esegui un solo Agent Package in questa chat.
- Segui prima runtime-adapters/codex.md e runtime-adapters/manual-execution.md.
- Leggi tutti gli input indicati nell'Agent Package prima di modificare file.
- Controlla gli Human Gate nel Project Workspace prima di procedere.
- Se un Human Gate Pending blocca il task corrente, fermati e segnala stato blocked.
- Rispetta boundaries, responsibilities, workflow e Definition of Done dell'Agent Package.
- Non modificare standard permanenti, archetype, capability o agenti permanenti salvo istruzione esplicita nell'Agent Package.
- Produci solo gli output richiesti dall'Agent Package.
- Produci handoff conforme a standards/handoff-standard.md se richiesto.
- Se emerge una lezione riutilizzabile, crea una Knowledge Candidate invece di integrare direttamente la conoscenza permanente.
- Alla fine riepiloga stato finale, file creati/modificati, verifiche eseguite, blocchi e rischi residui.
```

## Failure Mode Da Evitare

- Usare una chat Codex per eseguire piu Agent Package senza handoff.
- Saltare Human Gate perche la decisione sembra ovvia.
- Modificare conoscenza permanente mentre si esegue un agente temporaneo.
- Allargare il task oltre l'Agent Package.
- Produrre output richiesti ma dimenticare handoff.
- Creare Knowledge Candidate e poi integrarla direttamente.
- Confondere review approval con Human Gate approval.

## Criteri Di Completamento Dell'Adapter

Questo adapter e applicato correttamente quando:

1. il prompt include repository, Agent Package, Execution Blueprint e Project Workspace;
2. Codex legge adapter, package, blueprint, capability e standard rilevanti;
3. Human Gate sono controllati prima delle modifiche;
4. Codex modifica solo file coerenti con l'Agent Package;
5. output e handoff richiesti sono prodotti;
6. eventuali Knowledge Candidate restano nel Project Workspace;
7. la risposta finale dichiara stato, verifiche e rischi.
