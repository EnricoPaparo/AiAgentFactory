# Project Workspace Guide

Questo file è la guida operativa per avviare e gestire un Project Workspace nella factory.

Copiare `projects/_template/` in `projects/<project-id>/` come primo passo di ogni nuovo progetto.

---

## Prerequisiti

Prima di avviare un progetto, verificare che esistano:

- [ ] Tutti gli standard in `standards/` (MVP 1 completato)
- [ ] Tutti gli agenti permanenti in `agents/` (MVP 2 completato)
- [ ] Gli archetype necessari in `archetypes/` (MVP 3 completato)
- [ ] Almeno un runtime adapter in `runtime-adapters/`
- [ ] Una richiesta iniziale comprensibile con obiettivo e output atteso

---

## Struttura del Workspace

```text
projects/<project-id>/
├── README.md                  # questo file
├── project-status.md          # stato corrente del progetto
├── input/                     # richiesta iniziale e materiali di contesto
├── blueprints/                # Requirements, Solution, Execution Blueprint
├── generated-agents/          # Agent Package pronti per l'esecuzione
├── handoffs/                  # contratti di passaggio tra agenti o fasi
├── human-gates/               # punti di controllo bloccanti con decisione umana
├── deliverables/              # output finali del progetto
├── reviews/                   # report di review tecnica
└── knowledge-candidates/      # proposte di miglioramento per Knowledge Evolution
```

---

## Flusso Operativo Passo per Passo

### Passo 1 — Input

Creare `input/initial-request.md` con:
- Cosa l'utente o lo stakeholder vuole ottenere
- Vincoli noti (tempo, tecnologia, budget, team)
- Contesto rilevante o artefatti esistenti
- Ambiguità già identificate

Il file di input non è un blueprint — è la materia grezza che il Requirement Analyst trasformerà in requisiti strutturati.

### Passo 2 — Requirements Blueprint

Attivare il **Requirement Analyst** (`agents/requirement-analyst/`).

Output atteso: `blueprints/requirements-blueprint.md`

Il Requirements Blueprint deve contenere (vedi `standards/requirements-blueprint-standard.md`):
- Obiettivo
- Requisiti funzionali e non funzionali
- Vincoli e assunzioni
- Ambiguità registrate
- Fuori scope
- Criteri di accettazione
- Rischi iniziali

**Criterio di avanzamento:** il Requirements Blueprint contiene tutti i campi obbligatori dello standard e ogni requisito funzionale è verificabile.

### Passo 3 — Solution Blueprint

Attivare l'**Architect** (`agents/architect/`).

Input: `blueprints/requirements-blueprint.md`  
Output atteso: `blueprints/solution-blueprint.md`

Il Solution Blueprint deve contenere (vedi `standards/solution-blueprint-standard.md`):
- Architettura proposta
- Stack tecnologico
- Componenti e integrazioni
- Trade-off e alternative scartate
- Rischi tecnici
- Strategia implementativa

**Criterio di avanzamento:** il Solution Blueprint risponde a tutti i requisiti e vincoli del Requirements Blueprint.

### Passo 4 — Execution Blueprint

Attivare il **Pipeline Designer** (`agents/pipeline-designer/`).

Input: `blueprints/requirements-blueprint.md`, `blueprints/solution-blueprint.md`  
Output atteso: `blueprints/execution-blueprint.md`

L'Execution Blueprint deve contenere (vedi `standards/execution-blueprint-standard.md`):
- Team richiesto (agenti, sorgenti, capability)
- Workflow con sequenza e parallelismo
- Handoff tra agenti
- Review gate
- Human Gate con blocking scope
- Criteri di completamento del progetto
- Regole di escalation

**Criterio di avanzamento:** ogni agente nel team ha responsabilità non sovrapposte, ogni Human Gate ha un blocking scope definito.

### Passo 5 — Generazione Agent Package

Attivare il **Knowledge Compiler** (`agents/knowledge-compiler/`).

Input: `blueprints/execution-blueprint.md`, archetype, capability  
Output atteso: uno o più file in `generated-agents/`

Ogni Agent Package deve essere valido secondo `standards/agent-package-standard.md`.

**Criterio di avanzamento:** ogni Agent Package ha ruolo, missione, input, output, limiti, capability, workflow e Definition of Done verificabile.

### Passo 6 — Esecuzione

Tradurre ogni Agent Package tramite il runtime adapter appropriato (vedi `runtime-adapters/`).

Per ogni agente eseguito:
1. Seguire le istruzioni del runtime adapter scelto
2. Rispettare i limiti e le regole dell'Agent Package
3. Produrre un handoff conforme a `standards/handoff-standard.md` al termine
4. Depositare il handoff in `handoffs/`

**Regola critica:** se un Human Gate in `human-gates/` è in stato `Pending`, nessun task nel suo `blocking-scope` può essere eseguito. Attendere la decisione umana.

### Passo 7 — Review e Gate

Attivare gli agenti di review (Reviewer, Tester, Security Auditor) secondo quanto definito nell'Execution Blueprint.

Output: report di review in `reviews/`

Ogni review gate dichiarato nell'Execution Blueprint deve essere eseguito. Un review gate non eseguito è un failure mode della factory.

### Passo 8 — Supervisione

Attivare il **Pipeline Supervisor** (`agents/pipeline-supervisor/`).

Il Pipeline Supervisor verifica:
- Presenza e completezza degli handoff
- Esecuzione dei review gate
- Rispetto dei Human Gate
- Corrispondenza tra output prodotti e criteri di completamento dell'Execution Blueprint

Output: approvazione finale o richiesta di revisione.

### Passo 9 — Knowledge Candidates

Raccogliere tutte le Knowledge Candidate prodotte durante il progetto in `knowledge-candidates/`.

Attivare il **Knowledge Evolution** (`agents/knowledge-evolution/`) per valutare ogni proposta.

Per ogni Knowledge Candidate:
- Se approvata: Knowledge Evolution integra la conoscenza nei file permanenti corretti
- Se respinta: la motivazione viene registrata nel file della Knowledge Candidate
- Aggiornare lo stato nel file: `Proposed` → `Reviewed` → `Accepted` → `Integrated` / `Rejected`

### Passo 10 — Chiusura

Aggiornare `project-status.md` con:
- Stato finale: Completato / Interrotto / In attesa
- Deliverable prodotti e collegamento ai criteri di accettazione
- Knowledge Candidate prodotte e loro esito
- Lezioni apprese non catturate come Knowledge Candidate

Il Project Workspace può essere archiviato quando:
- tutti i deliverable sono presenti
- tutti i review gate sono stati eseguiti
- tutti gli handoff finali sono presenti
- tutte le Knowledge Candidate hanno uno stato diverso da `Proposed`

---

## Regole Invarianti del Workspace

1. **Conoscenza temporanea.** Il Project Workspace contiene lavoro temporaneo, non conoscenza permanente approvata.
2. **Human Gate bloccante.** Un Human Gate `Pending` blocca tutti i task nel suo `blocking-scope`. Non esistono eccezioni.
3. **Handoff obbligatorio.** Ogni passaggio tra agenti o fasi produce un handoff verificabile conforme allo standard.
4. **Knowledge Candidate prima di integrare.** Nessuna modifica alla conoscenza permanente avviene direttamente dal workspace.
5. **Review gate non saltabili.** Ogni review gate dichiarato nell'Execution Blueprint deve essere eseguito, non solo dichiarato.
6. **Deliverable collegati ai criteri.** I deliverable finali devono essere esplicitamente collegati ai criteri di accettazione del Requirements Blueprint.

---

## Aggiornamento di project-status.md

Il file `project-status.md` deve riflettere lo stato corrente del progetto in ogni momento.

Campi consigliati:

```markdown
# Project Status: <project-id>

## Stato corrente
[In corso / In attesa Human Gate / In review / Completato / Interrotto]

## Fase corrente
[quale passo del flusso è attivo]

## Human Gate aperti
[elenco di human-gates/ in stato Pending con blocking-scope]

## Agenti attivi
[quale Agent Package è in esecuzione]

## Deliverable prodotti
[elenco con stato: prodotto / in revisione / approvato]

## Knowledge Candidate
[elenco con stato corrente]

## Ultimo aggiornamento
[data e agente che ha aggiornato]
```

---

## Riferimenti

| Documento | Scopo |
|---|---|
| `standards/agent-package-standard.md` | Formato Agent Package |
| `standards/handoff-standard.md` | Formato handoff |
| `standards/human-gate-standard.md` | Formato e regole Human Gate |
| `standards/requirements-blueprint-standard.md` | Formato Requirements Blueprint |
| `standards/solution-blueprint-standard.md` | Formato Solution Blueprint |
| `standards/execution-blueprint-standard.md` | Formato Execution Blueprint |
| `standards/knowledge-candidate-standard.md` | Formato Knowledge Candidate |
| `runtime-adapters/manual-execution.md` | Esecuzione manuale senza orchestratore |
| `GLOSSARY.md` | Definizioni di tutti i termini |
