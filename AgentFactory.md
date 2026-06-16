# AgentFactory

AgentFactory è un repository di conoscenza strutturata per progettare, generare, orchestrare, supervisionare, evolvere e distruggere team temporanei di agenti AI specializzati nello sviluppo di progetti software.

AgentFactory non è un runtime, non è un framework applicativo, non è una pipeline Python e non è una raccolta generica di prompt. È il riferimento architetturale della factory: definisce identità, confini, componenti, workflow, contratti e regole invarianti. Gli standard operativi dei singoli artefatti vivono in `standards/`.

---

# 1. Scopo del progetto

L'obiettivo è costruire una fabbrica di agenti capace di:

1. ricevere una richiesta di progetto;
2. trasformarla in requisiti;
3. progettare una soluzione;
4. progettare una pipeline di lavoro;
5. generare agenti temporanei specializzati;
6. eseguire il lavoro tramite uno o più runtime;
7. supervisionare output, handoff e review;
8. raccogliere lezioni apprese;
9. migliorare progressivamente la conoscenza permanente.

Il patrimonio principale della factory non sono gli agenti temporanei, ma la conoscenza permanente che permette di generare agenti migliori nel tempo.

---

# 2. Confini

AgentFactory non è:

* un'applicazione pronta all'uso;
* un orchestratore già implementato;
* un framework legato a Python o a un altro linguaggio;
* una copia di Claude Code, Codex, OpenCode o strumenti simili;
* un sistema vincolato a uno specifico modello AI;
* un tutorial di programmazione.

AgentFactory definisce l'architettura della conoscenza e del processo. L'implementazione tecnica viene dopo e deve poter cambiare senza riscrivere la factory.

---

# 3. Principi invarianti

Queste regole devono rimanere valide anche se cambiano runtime, modelli AI, strumenti o linguaggi.

1. La conoscenza permanente è la risorsa principale della factory.
2. Gli agenti di progetto sono istanze temporanee, create per uno specifico progetto o task.
3. Un subagente temporaneo può nascere da un archetype esistente oppure da una definizione ad hoc nell'Execution Blueprint, insieme a capability pertinenti e contesto del task.
4. I runtime sono intercambiabili e non devono contenere la logica principale della factory.
5. Prima si definiscono ruoli, responsabilità, contratti e workflow; poi si decide come eseguirli tecnicamente.
6. Il codice è uno strumento operativo, non il centro della factory.
7. Ogni passaggio importante deve avere input, output, responsabilità e criteri di completamento chiari.
8. Nessuna proposta generata durante un progetto modifica automaticamente la conoscenza permanente.
9. Il Project Workspace contiene lavoro temporaneo, non conoscenza approvata.
10. Il Pipeline Supervisor valida il processo e i gate di controllo; non deve diventare un super-agente tecnico onnisciente.

---

# 4. Concetti chiave

| Concetto | Definizione |
|---|---|
| Agenti permanenti | Ruoli stabili della factory. Definiscono e governano il processo principale. |
| Factory Intake | Agente permanente che riceve una richiesta grezza, crea il Project Workspace iniziale e prepara il primo Agent Package per Requirement Analyst. |
| Factory Host | Agente permanente conversazionale che coordina fasi, Agent Package, handoff e Human Gate nella stessa sessione runtime. |
| Factory Runner | Agente permanente operativo che usa stato macchina, artifact index e runtime packet per rendere il flusso riprendibile e token-efficient. |
| Subagenti temporanei | Agenti creati per uno specifico progetto o task. Possono essere archiviati o distrutti a fine lavoro. |
| Archetype | Scheletro riutilizzabile e approvato per generare subagenti temporanei di un tipo ricorrente. Definisce ruolo, responsabilità, input, output, limiti e formato dei deliverable. Non contiene conoscenza tecnica specifica e non limita la creazione di agenti ad hoc. |
| Capability | Conoscenza tecnica operativa riutilizzabile: best practice, checklist, failure mode, rischi, criteri di revisione e lezioni apprese. Non è un tutorial. |
| Agent Package | Pacchetto operativo che descrive un agente pronto per essere eseguito da un runtime. È indipendente dal runtime. |
| Runtime Packet | Contesto compatto, task-specifico, generato per eseguire un Agent Package senza rileggere tutta la factory. |
| Knowledge Compiler | Strato concettuale che compone Agent Package a partire da archetype o definizioni ad hoc, capability, contesto progetto, task e criteri di completamento. |
| Runtime Adapter | Regole di adattamento che traducono un Agent Package generico nel formato richiesto da uno specifico runtime. |
| Project Workspace | Spazio temporaneo del progetto: input, blueprint, agenti generati, handoff, deliverable, review e Knowledge Candidate. |
| Knowledge Candidate | Proposta di miglioramento nata durante un progetto. Può diventare conoscenza permanente solo dopo valutazione e approvazione. |
| Handoff | Consegna formale tra agenti o fasi. Deve rendere verificabile cosa è stato prodotto e cosa deve accadere dopo. |
| Human Gate | Punto di controllo in cui la factory deve fermarsi e attendere una decisione umana prima di proseguire. |
| Factory State | Stato macchina compatto del Project Workspace, usato dal runtime per sapere fase, gate pending e prossima azione. |

---

# 5. Flusso end-to-end

```text
User Request
→ Factory Host
→ Factory Runner
→ Factory Intake
→ Project Bootstrap
→ Requirement Analyst
→ Requirements Blueprint
→ Architect
→ Solution Blueprint
→ Pipeline Designer
→ Execution Blueprint
→ Knowledge Compiler
→ Agent Package temporanei
→ Runtime Packet
→ Runtime Adapter
→ Project Team Execution
→ Pipeline Supervisor Review
→ Knowledge Evolution
→ aggiornamento controllato della conoscenza permanente
```

Questo flusso separa analisi, progettazione, generazione degli agenti, esecuzione, supervisione ed evoluzione della conoscenza. La separazione riduce ambiguità, sovrapposizioni e dipendenza dal runtime.

---

# 6. Agenti permanenti

| Agente | Input principale | Output principale | Responsabilità | Limite |
|---|---|---|---|---|
| Factory Intake | Richiesta utente grezza | Project Workspace iniziale, bootstrap blueprint, Requirement Analyst Agent Package | Preserva la richiesta, crea il workspace e prepara il primo run della factory. | Non produce requisiti, architettura, execution plan o deliverable. |
| Factory Host | Richiesta utente o Project Workspace | Stato conversazionale, avanzamento fasi, richieste Human Gate, handoff | Coordina gli agenti e mantiene il processo nella stessa conversazione runtime. | Non sostituisce agenti specialistici e non decide Human Gate. |
| Factory Runner | Factory State, Project Workspace, gate e artifact index | Prossima azione, runtime context minimo, stato aggiornato | Riduce inferenza e token decidendo la prossima fase da stato macchina. | Non sostituisce agenti specialistici e non decide Human Gate. |
| Requirement Analyst | Richiesta utente | Requirements Blueprint | Chiarisce obiettivi, requisiti, vincoli, ambiguità, assunzioni e criteri di accettazione. | Non sceglie stack, architettura o agenti. |
| Architect | Requirements Blueprint | Solution Blueprint | Propone architettura, stack, componenti, integrazioni, rischi tecnici e trade-off. | Non crea il team operativo e non implementa codice. |
| Pipeline Designer | Requirements Blueprint, Solution Blueprint | Execution Blueprint | Progetta task force, workflow, handoff, review gate, responsabilità e criteri di completamento. | Non esegue direttamente il progetto e non aggiorna la knowledge base. |
| Knowledge Compiler | Execution Blueprint, archetype o definizioni ad hoc, capability, contesto, task | Agent Package temporanei | Compone agenti coerenti, pertinenti e utilizzabili dal runtime. | Non decide strategia progettuale e non supervisiona l'esecuzione. |
| Pipeline Supervisor | Execution Blueprint, handoff, deliverable, review | Approvazioni, blocchi, richieste di revisione | Verifica rispetto del processo, presenza degli output, coerenza degli handoff e completamento dei review gate. | Non sostituisce Developer, Tester, Reviewer o Security Auditor. |
| Knowledge Evolution | Knowledge Candidate | Proposte accettate, respinte o integrate | Classifica e valuta le proposte, distinguendo conoscenza locale da conoscenza riutilizzabile. | Non integra automaticamente ogni proposta. |

---

# 7. Subagenti temporanei

I subagenti temporanei sono creati per uno specifico progetto o task. Esempi:

* Developer;
* Tester;
* Reviewer;
* Security Auditor;
* Documentation Writer;
* DevOps Specialist.

Un subagente temporaneo nasce dalla combinazione di una sorgente di ruolo, capability pertinenti e contesto operativo.

La sorgente di ruolo può essere:

* un archetype esistente, quando il ruolo è ricorrente e stabilizzato;
* una definizione ad hoc nell'Execution Blueprint, quando il ruolo è nuovo, raro o sperimentale.

Un agente ad hoc può generare una Knowledge Candidate per creare un nuovo archetype se dimostra utilità riutilizzabile.

Composizione tipica da archetype:

```text
archetype esistente
+ capability pertinenti
+ contesto del progetto
+ task corrente
+ tool disponibili
+ regole operative
+ criteri di completamento
```

Composizione tipica da definizione ad hoc:

```text
definizione ad hoc nell'Execution Blueprint
+ capability pertinenti
+ contesto del progetto
+ task corrente
+ tool disponibili
+ regole operative
+ criteri di completamento
= Agent Package temporaneo
```

Esempio:

```text
archetypes/developer.md
+ capabilities/node.md
+ capabilities/postgres.md
+ contesto progetto
+ task corrente
= projects/project-name/generated-agents/developer-node-postgres.md
```

Il file generato è un Agent Package temporaneo. Può essere usato da un Runtime Adapter per eseguire il lavoro in Claude Code, Codex, OpenCode, OpenAI Agents SDK, LangGraph, esecuzione manuale o runtime futuri.

---

# 8. Artefatti principali

| Artefatto | Creato da | Usato da | Contenuto essenziale |
|---|---|---|---|
| Requirements Blueprint | Requirement Analyst | Architect, Pipeline Designer | Obiettivo, requisiti funzionali e non funzionali, vincoli, assunzioni, ambiguità, criteri di accettazione, fuori scope, rischi iniziali. |
| Project Bootstrap | Factory Intake | Requirement Analyst, Runtime Adapter, maintainer umano | Project Workspace iniziale, richiesta originale, bootstrap blueprint, primo Agent Package e prompt di avvio. |
| Solution Blueprint | Architect | Pipeline Designer | Architettura, stack, componenti, flussi dati, integrazioni, sicurezza, trade-off, rischi tecnici, alternative scartate, strategia implementativa. |
| Execution Blueprint | Pipeline Designer | Knowledge Compiler, Pipeline Supervisor | Team richiesto, archetype o definizioni ad hoc, capability, workflow, handoff, responsabilità, review gate, human gate, escalation, criteri di completamento. |
| Agent Package | Knowledge Compiler | Runtime Adapter, Project Team | Identità, missione, input, output, responsabilità, limiti, conoscenza assegnata, tool, workflow, handoff, Definition of Done. |
| Runtime Packet | Knowledge Compiler o Factory Runner | Runtime Adapter, Project Team | Task, contesto approvato minimo, file da leggere, vincoli, output, gate status e budget contesto. |
| Handoff | Agente o fase mittente | Agente o fase destinataria, Supervisor | Output consegnato, decisioni prese, file coinvolti, rischi residui, problemi aperti, prossima azione. |
| Review Report | Tester, Reviewer, Auditor o altro agente tecnico | Pipeline Supervisor | Esito controlli, problemi rilevati, gravità, raccomandazioni, approvazione o blocco. |
| Human Gate | Pipeline Designer o Pipeline Supervisor | Pipeline Supervisor, Runtime Adapter, maintainer umano | Decisione richiesta, contesto, opzioni, criteri di approvazione, blocking scope, decisione umana. |
| Factory State | Factory Intake o Factory Runner | Factory Host, Runtime Adapter, Pipeline Supervisor | Fase corrente, status, pending gate, prossima azione, summaries approvate e runtime packet disponibili. |
| Knowledge Candidate | Qualsiasi agente o fase | Knowledge Evolution | Proposta di miglioramento, contesto, motivazione, rischio, generalizzabilità, destinazione proposta. |

---

# 9. Handoff minimo

Ogni handoff deve contenere almeno:

* mittente;
* destinatario;
* task o fase completata;
* output prodotto;
* file o artefatti coinvolti;
* decisioni prese;
* problemi aperti;
* rischi residui;
* prossima azione richiesta;
* criteri per verificare l'output.

Un handoff non è un semplice messaggio descrittivo. È un contratto di passaggio tra una responsabilità e la successiva.

---

# 10. Definition of Ready e Definition of Done

## Progetto ready

Un progetto è pronto per entrare nella factory quando esistono almeno:

* richiesta iniziale;
* obiettivo identificabile;
* output atteso comprensibile;
* vincoli noti o dichiarati come assunzioni;
* ambiguità principali registrate.

## Agent Package ready

Un Agent Package è pronto quando contiene almeno:

* ruolo;
* missione;
* task assegnato;
* input disponibili;
* output atteso;
* limiti operativi;
* capability assegnate;
* tool disponibili;
* handoff richiesti;
* criteri di completamento.

## Progetto done

Un progetto è completato quando:

* i deliverable previsti sono prodotti;
* i review gate sono stati eseguiti;
* i criteri di accettazione sono stati verificati;
* gli handoff finali sono presenti;
* le Knowledge Candidate sono state raccolte;
* il workspace può essere archiviato.

---

# 11. Ciclo di vita delle Knowledge Candidate

Una Knowledge Candidate può trovarsi in uno di questi stati:

| Stato | Significato |
|---|---|
| Proposed | La proposta è stata generata durante il progetto. |
| Reviewed | La proposta è stata analizzata per utilità, rischio, generalizzabilità e impatto. |
| Accepted | La proposta è ritenuta utile e riutilizzabile. |
| Integrated | La proposta è stata integrata nei file permanenti corretti. |
| Rejected | La proposta è stata respinta con motivazione. |
| Deprecated | Una conoscenza precedentemente valida non è più consigliata, ma resta tracciata. |

Una proposta può riguardare archetype, capability, agenti permanenti, skill operative, regole di processo, failure mode, checklist, standard o runtime adapter.

---

# 12. Struttura del repository

```text
AgentFactory/
├── README.md
├── AgentFactory.md
├── agents/
│   ├── factory-intake/
│   ├── factory-host/
│   ├── factory-runner/
│   ├── requirement-analyst/
│   │   ├── requirement-analyst.md
│   │   └── requirement-analyst-skills.md
│   ├── architect/
│   ├── pipeline-designer/
│   ├── pipeline-supervisor/
│   └── knowledge-evolution/
├── archetypes/
│   ├── developer.md
│   ├── tester.md
│   ├── reviewer.md
│   ├── security-auditor.md
│   └── documentation-writer.md
├── capabilities/
│   ├── node.md
│   ├── java.md
│   ├── postgres.md
│   ├── docker.md
│   └── react.md
├── standards/
│   ├── agent-package-standard.md
│   ├── factory-state-standard.md
│   ├── runtime-packet-standard.md
│   ├── project-bootstrap-standard.md
│   ├── handoff-standard.md
│   ├── human-gate-standard.md
│   ├── capability-standard.md
│   ├── requirements-blueprint-standard.md
│   ├── solution-blueprint-standard.md
│   ├── execution-blueprint-standard.md
│   └── knowledge-candidate-standard.md
├── runtime-adapters/
│   ├── claude-code.md
│   ├── codex.md
│   ├── codex-conversation.md
│   ├── codex-project-bootstrap.md
│   ├── opencode.md
│   ├── openai-agents-sdk.md
│   ├── langgraph.md
│   └── manual-execution.md
└── projects/
    └── _template/
        ├── input/
        ├── blueprints/
        ├── summaries/
        ├── generated-agents/
        ├── runtime-packets/
        ├── handoffs/
        ├── human-gates/
        ├── deliverables/
        ├── reviews/
        └── knowledge-candidates/
```

---

# 13. Cartelle principali

| Cartella | Scopo |
|---|---|
| `agents/` | Contiene gli agenti permanenti della factory. Ogni agente ha un file identità/comportamento e un file skill/conoscenza operativa. |
| `archetypes/` | Contiene gli scheletri dei subagenti temporanei. Definisce ruoli, non conoscenza tecnica specifica. |
| `capabilities/` | Contiene conoscenza tecnica operativa riutilizzabile da più agenti e progetti. Non contiene tutorial generici. |
| `standards/` | Contiene i formati minimi obbligatori degli artefatti principali. Serve a evitare ambiguità tra agenti. |
| `runtime-adapters/` | Contiene le regole di traduzione da Agent Package generico a runtime specifico. Non contiene logica decisionale della factory. |
| `projects/` | Contiene workspace temporanei di progetto. Non rappresenta conoscenza permanente. |

---

# 14. Dove mettere cosa

| Tipo di conoscenza | Destinazione |
|---|---|
| Regola di comportamento del Requirement Analyst | `agents/requirement-analyst/` |
| Regola di bootstrap di un nuovo progetto | `agents/factory-intake/` |
| Regola di coordinamento conversazionale | `agents/factory-host/` |
| Regola di avanzamento da stato macchina | `agents/factory-runner/` |
| Skill operativa stabile di un agente permanente | `agents/<agent-name>/<agent-name>-skills.md` |
| Regola generale su come lavora un Developer temporaneo | `archetypes/developer.md` |
| Conoscenza tecnica su PostgreSQL | `capabilities/postgres.md` |
| Formato obbligatorio di un Agent Package | `standards/agent-package-standard.md` |
| Formato obbligatorio dello stato macchina | `standards/factory-state-standard.md` |
| Formato obbligatorio di un runtime packet | `standards/runtime-packet-standard.md` |
| Formato obbligatorio del bootstrap progetto | `standards/project-bootstrap-standard.md` |
| Formato obbligatorio di un handoff | `standards/handoff-standard.md` |
| Regola di adattamento per Claude Code | `runtime-adapters/claude-code.md` |
| Decisione valida solo per un progetto | `projects/<project-name>/` |
| Proposta di miglioramento non ancora approvata | `projects/<project-name>/knowledge-candidates/` |

Regola guida: se una conoscenza è locale, resta nel Project Workspace; se è riutilizzabile, diventa Knowledge Candidate; se è approvata, entra nella conoscenza permanente.

---

# 15. Regole di naming

* usare `kebab-case` per file e cartelle;
* agenti permanenti in `agents/<agent-name>/`;
* archetype al singolare: `developer.md`, `tester.md`;
* capability per tecnologia, dominio o pratica: `postgres.md`, `api-security.md`, `frontend-performance.md`;
* standard con suffisso `-standard.md`;
* progetti con nome descrittivo;
* Agent Package temporanei con pattern descrittivo, ad esempio `developer-node-postgres.md`.

---

# 16. Failure mode principali

La factory deve prevenire questi errori:

* agenti con responsabilità sovrapposte;
* archetype usati come vincolo rigido invece che come conoscenza riutilizzabile;
* capability troppo generiche o trasformate in tutorial;
* Agent Package troppo lunghi o pieni di contesto inutile;
* Factory Intake trasformato in super-agente che produce requisiti, architettura o deliverable;
* Factory Host trasformato in super-agente tecnico che salta gli agenti specialistici;
* Factory Runner che ricalcola stato e contesto leggendo tutto invece di usare `factory-state.json`;
* Knowledge Candidate integrate senza validazione;
* Pipeline Supervisor trasformato in super-agente tecnico;
* Runtime Adapter che assorbe logica decisionale;
* Project Workspace confuso con conoscenza permanente;
* blueprint incompleti usati come se fossero stabili;
* handoff vaghi o non verificabili;
* review gate dichiarati ma non eseguiti.
* Human Gate dichiarati ma bypassati o lasciati in `Pending` mentre il workflow prosegue.

---

# 17. MVP della factory

## MVP 1 - Standardizzazione

1. `agent-package-standard.md`
2. `handoff-standard.md`
3. `requirements-blueprint-standard.md`
4. `solution-blueprint-standard.md`
5. `execution-blueprint-standard.md`
6. `knowledge-candidate-standard.md`
7. `capability-standard.md`
8. `human-gate-standard.md`
9. `factory-state-standard.md`
10. `runtime-packet-standard.md`

## MVP 2 - Agenti permanenti

1. Factory Intake
2. Factory Host
3. Factory Runner
4. Requirement Analyst
5. Architect
6. Pipeline Designer
7. Pipeline Supervisor
8. Knowledge Evolution

## MVP 3 - Subagenti temporanei

1. Developer
2. Tester
3. Reviewer
4. Documentation Writer
5. Security Auditor

## MVP 4 - Prima esecuzione manuale

1. scegliere un progetto piccolo;
2. produrre Requirements Blueprint;
3. produrre Solution Blueprint;
4. produrre Execution Blueprint;
5. generare Agent Package;
6. eseguire tramite Manual Execution Adapter;
7. raccogliere Knowledge Candidate;
8. aggiornare solo la conoscenza approvata.

---

# 18. Stato attuale

Definito:

* obiettivo della factory;
* confini del progetto;
* principi invarianti;
* agenti permanenti;
* Factory Intake;
* Factory Host;
* Factory Runner;
* subagenti temporanei;
* archetype;
* capability;
* Agent Package;
* Knowledge Compiler;
* Runtime Adapter;
* Project Workspace;
* Knowledge Candidate Lifecycle;
* handoff minimo;
* struttura repository;
* MVP iniziale.

Implementato nella baseline operativa:

* standard principali;
* Factory Intake;
* agenti permanenti principali;
* archetype iniziali;
* capability iniziali;
* Manual Execution Adapter;
* Codex Runtime Adapter;
* Codex Conversation Adapter;
* Codex Project Bootstrap Adapter;
* Project Workspace Template;
* Factory State;
* Runtime Packet;
* primo pilota manuale.

Da sviluppare dopo la baseline:

* runner automatico o semi-automatico;
* adapter per altri runtime;
* validatori automatici degli artefatti;
* ulteriori capability tecniche;
* progetti pilota software piu realistici.

---

# 19. Prossimo passo

Il prossimo passo operativo è usare:

```text
runtime-adapters/codex-project-bootstrap.md
```

per avviare nuovi progetti da una richiesta grezza dell'utente.

Subito dopo il bootstrap, il primo agente da eseguire è:

```text
Requirement Analyst
```

Il Requirement Analyst produce il Requirements Blueprint e avvia il ciclo completo della factory.
