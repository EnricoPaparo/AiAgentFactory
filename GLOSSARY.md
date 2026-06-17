# Glossario

Definizioni precise di tutti i termini usati in AiAgentFactory. Quando un termine compare in qualsiasi documento della factory, ha esattamente il significato qui definito.

---

## Agent Package

Specifica operativa autonoma che descrive un agente temporaneo pronto per essere eseguito da un runtime adapter. Un Agent Package è indipendente dal runtime — non dipende da nessun ambiente di esecuzione specifico.

Un Agent Package è composto dal **Knowledge Compiler** a partire da:
- una sorgente di ruolo (archetype esistente o definizione ad hoc nell'Execution Blueprint)
- capability pertinenti
- contesto di progetto
- task assegnato
- strumenti disponibili
- regole operative
- criteri di completamento

Formato definito in: `standards/agent-package-standard.md`

---

## Archetype

Scheletro riutilizzabile e approvato per generare agenti temporanei di un tipo ricorrente. Un archetype definisce ruolo, responsabilità, input, output, confini e Definition of Done. **Non** contiene conoscenza tecnica specifica (quella appartiene alle capability). Gli archetype sono un punto di partenza, non un vincolo — il Pipeline Designer può definire agenti ad hoc quando nessun archetype esistente è adatto.

Archiviati in: `archetypes/`

---

## Capability

Pacchetto di conoscenza operativa riutilizzabile per una tecnologia, un dominio o una pratica specifica. Le capability contengono best practice, checklist, failure mode, rischi e criteri di revisione. **Non** sono tutorial o introduzioni — sono riferimenti operativi che gli agenti usano durante l'esecuzione di un task.

Le capability vengono assegnate agli agenti temporanei nell'Agent Package. Più capability possono essere combinate.

Esempi: `node.md`, `api-security.md`, `git-workflow.md`

Formato definito in: `standards/capability-standard.md`
Archiviate in: `capabilities/`

---

## Definition of Done (DoD)

Insieme di condizioni verificabili che determinano quando un task o un artefatto è completo. Ogni agente permanente, archetype e Agent Package deve definire una Definition of Done. Il Pipeline Supervisor usa la DoD per verificare il completamento del task senza sostituirsi all'agente tecnico.

---

## Execution Blueprint

Il piano operativo di un progetto. Definisce il team di agenti (ruoli, sorgenti, capability), il workflow (sequenza, parallelismo), le assegnazioni di handoff, i gate di revisione, i Human Gate e i criteri di completamento. L'Execution Blueprint è prodotto dal **Pipeline Designer** e consumato dal **Knowledge Compiler** e dal **Pipeline Supervisor**.

Formato definito in: `standards/execution-blueprint-standard.md`

---

## Handoff

Contratto di consegna formale tra agenti o fasi. Un handoff non è un riassunto narrativo — è un trasferimento verificabile di responsabilità. Ogni handoff deve dichiarare: cosa è stato completato, cosa è stato prodotto, quali file sono stati toccati, quali decisioni sono state prese, quali problemi rimangono aperti, rischi residui, l'azione successiva richiesta e i criteri per verificare l'output.

Un handoff mancante o vago è un failure mode della factory.

Formato definito in: `standards/handoff-standard.md`

---

## Human Gate

Punto di decisione obbligatorio in cui la factory deve fermarsi e attendere una decisione umana prima di procedere. I Human Gate sono definiti dal **Pipeline Designer** e imposti dal **Pipeline Supervisor** e dai runtime adapter.

**Invariante chiave:** Quando un Human Gate è `Pending`, **nessun task nel suo `blocking-scope` dichiarato può essere eseguito**. Non ci sono eccezioni.

Stati del Human Gate: `Pending` → `Approved` / `Rejected` / `Changes Requested` / `Expired` / `Cancelled`

Formato definito in: `standards/human-gate-standard.md`

---

## Knowledge Candidate

Proposta di miglioramento strutturata generata durante un progetto. Qualsiasi agente o fase può produrre una Knowledge Candidate quando identifica una lezione riutilizzabile, una nuova best practice, un failure mode o una lacuna nella conoscenza esistente.

Le Knowledge Candidate sono artefatti temporanei — vivono nel project workspace. Diventano conoscenza permanente **solo** dopo la valutazione e l'approvazione da parte dell'agente **Knowledge Evolution**.

Stati: `Proposta` → `Revisionata` → `Accettata` → `Integrata`
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;`→ Rifiutata`

Formato definito in: `standards/knowledge-candidate-standard.md`

---

## Knowledge Compiler

Agente permanente responsabile della composizione degli Agent Package. Il Knowledge Compiler legge un Execution Blueprint, seleziona o riceve archetype o definizioni ad hoc, assegna capability pertinenti e assembla Agent Package completi ed eseguibili. Non prende decisioni strategiche di progetto e non supervisiona l'esecuzione.

Definito in: `agents/knowledge-compiler/`

---

## Knowledge Evolution

Agente permanente responsabile della valutazione delle Knowledge Candidate e della decisione su quali diventano conoscenza permanente. Knowledge Evolution distingue tra conoscenza localmente utile (rimane nel progetto) e conoscenza genuinamente riutilizzabile (promossa a file permanenti). Non integra mai una proposta automaticamente.

Definito in: `agents/knowledge-evolution/`

---

## Agente Permanente

Ruolo stabile di governance nella factory. Gli agenti permanenti definiscono e governano il processo centrale della factory — non svolgono lavoro di implementazione di progetto. I sei agenti permanenti sono: Requirement Analyst, Architect, Pipeline Designer, Knowledge Compiler, Pipeline Supervisor e Knowledge Evolution.

Gli agenti permanenti hanno una singola responsabilità chiaramente delimitata. Non si sovrappongono.

Archiviati in: `agents/`

---

## Pipeline Designer

Agente permanente che trasforma Requirements Blueprint e Solution Blueprint in un Execution Blueprint. Il Pipeline Designer progetta il team di agenti, il workflow, gli handoff, i gate di revisione e i Human Gate. Non esegue il progetto e non modifica la conoscenza permanente.

Definito in: `agents/pipeline-designer/`

---

## Pipeline Supervisor

Agente permanente che verifica la conformità del processo durante e dopo l'esecuzione del progetto. Il Pipeline Supervisor controlla che gli handoff siano presenti e completi, che i gate di revisione siano stati eseguiti, che i Human Gate siano stati rispettati e che i criteri di completamento siano soddisfatti. **Non** si sostituisce agli agenti tecnici (Developer, Tester, Reviewer, ecc.) — valida il processo, non la correttezza tecnica.

Definito in: `agents/pipeline-supervisor/`

---

## Project Workspace

Directory di lavoro temporanea per un progetto specifico. Contiene tutti gli artefatti specifici del progetto: input, blueprint, Agent Package generati, handoff, Human Gate, deliverable, review e Knowledge Candidate. I Project Workspace contengono **solo conoscenza temporanea** — le modifiche alla conoscenza permanente approvata passano per Knowledge Evolution.

Template: `projects/_template/`
Archiviati in: `projects/<project-id>/`

---

## Requirements Blueprint

Artefatto strutturato prodotto dal Requirement Analyst a partire da una richiesta utente. Contiene: obiettivo, requisiti funzionali e non funzionali, vincoli, assunzioni, ambiguità, elementi fuori scope, criteri di accettazione e rischi iniziali. **Non** contiene decisioni architetturali o scelte di stack.

Formato definito in: `standards/requirements-blueprint-standard.md`

---

## Review Gate

Checkpoint obbligatorio in cui un agente tecnico (Reviewer, Tester, Security Auditor, ecc.) verifica un output specifico prima che il workflow possa avanzare. I Review Gate sono dichiarati nell'Execution Blueprint e imposti dal Pipeline Supervisor. Un Review Gate dichiarato ma non eseguito è un failure mode della factory.

---

## Runtime Adapter

Insieme di regole di traduzione che convertono un Agent Package generico nel formato e nel modello di esecuzione richiesto da un runtime specifico (es. OpenCode, esecuzione manuale, Claude Code, OpenAI Agents SDK, LangGraph). I Runtime Adapter traducono — non contengono logica decisionale della factory. La logica centrale della factory (ruoli, standard, handoff, gate) rimane invariata indipendentemente dal runtime adapter usato.

Archiviati in: `runtime-adapters/`

---

## Solution Blueprint

Artefatto di progettazione tecnica prodotto dall'Architect a partire da un Requirements Blueprint. Contiene: architettura proposta, stack tecnologico, componenti, flussi di dati, integrazioni, strategia di sicurezza, trade-off, alternative scartate, rischi tecnici e strategia di implementazione. L'Architect non costruisce il team di agenti — quello è il lavoro del Pipeline Designer.

Formato definito in: `standards/solution-blueprint-standard.md`

---

## Subagente (Agente Temporaneo)

Agente creato per un progetto o task specifico. I subagenti sono usa e getta — possono essere archiviati o eliminati al termine del progetto. Vengono composti dal Knowledge Compiler a partire da un archetype o una definizione ad hoc, più capability pertinenti e contesto di progetto.

I subagenti si distinguono dagli Agenti Permanenti: svolgono lavoro di progetto, non governance della factory.

---

## Conoscenza Temporanea vs Permanente

| | Conoscenza Temporanea | Conoscenza Permanente |
|---|---|---|
| **Vive in** | `projects/<project-id>/` | `agents/`, `archetypes/`, `capabilities/`, `standards/`, `runtime-adapters/` |
| **Scope** | Un progetto o task | Tutti i progetti futuri |
| **Creata da** | Qualsiasi agente durante l'esecuzione | Knowledge Evolution (dopo approvazione) |
| **Sopravvive al progetto** | Archiviata, non promossa | Sì |
| **Porta d'ingresso** | Nessuna | Knowledge Candidate → Knowledge Evolution |

---

## Workflow

Sequenza operativa definita nell'Execution Blueprint che specifica l'ordine e il parallelismo degli agenti nel progetto. Esiste in due forme:
- **Execution Blueprint** (`blueprints/execution-blueprint.md`): documento human-readable che descrive strategia, agenti, input, output e gate.
- **workflow.yml** (`blueprints/workflow.yml`): versione machine-readable consumata da `tools/orchestrate.py` per l'esecuzione automatica della pipeline.
