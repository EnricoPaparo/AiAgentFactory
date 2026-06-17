# Contribuire ad AiAgentFactory

Questo documento spiega come estendere la conoscenza permanente della factory: aggiungere capability, archetype, standard, agenti permanenti e runtime adapter.

AiAgentFactory segue un **processo controllato di evoluzione della conoscenza**. Nessuna modifica alla conoscenza permanente deve avvenire senza una revisione deliberata. I miglioramenti spontanei appartengono prima alla cartella `knowledge-candidates/` del progetto.

---

## Regole Generali

1. **Tutte le modifiche permanenti passano per la revisione.** Usa una Knowledge Candidate durante l'esecuzione di un progetto, poi promuovila tramite l'agente Knowledge Evolution.
2. **Separazione delle responsabilità.** Non mettere conoscenza specifica di progetto nei file permanenti. Tieni il lavoro temporaneo in `projects/<project-id>/`.
3. **Nessuna integrazione automatica.** Anche se una modifica sembra ovviamente corretta, deve passare per il ciclo di vita Knowledge Evolution prima di atterrare nei file permanenti.
4. **Minimale ma completo.** Ogni nuovo artefatto deve soddisfare i campi obbligatori del suo standard. Preferire pochi file di alta qualità a molti file superficiali.
5. **Lingua.** Tutta la documentazione è scritta in **italiano**. I nuovi contributi devono seguire la stessa lingua.

---

## Convenzioni di Nomenclatura

| Tipo | Convenzione | Esempio |
|---|---|---|
| File e cartelle | `kebab-case` | `api-security.md`, `knowledge-compiler/` |
| Agenti permanenti | `agents/<nome-agente>/` | `agents/requirement-analyst/` |
| Archetype | sostantivo singolare | `developer.md`, `tester.md` |
| Capability | argomento o tecnologia | `postgres.md`, `api-security.md` |
| Standard | `<artefatto>-standard.md` | `handoff-standard.md` |
| Runtime adapter | nome del runtime | `claude-code.md`, `langgraph.md` |
| Agent Package | pattern descrittivo | `developer-node-postgres.md` |

---

## Come Aggiungere una Capability

Una capability è conoscenza operativa riutilizzabile — best practice, checklist, failure mode, rischi e lezioni apprese per una tecnologia, un dominio o una pratica specifica. **Non è** un tutorial.

**Campi obbligatori** (definiti in `standards/capability-standard.md`):
- Scopo
- Usata da
- Quando si usa
- Contenuto operativo (checklist, pratiche, failure mode, rischi)
- Criteri di revisione
- Limiti

**Passi:**
1. Verifica che la capability non esista già in `capabilities/`.
2. Crea `capabilities/<argomento>.md` seguendo `standards/capability-standard.md`.
3. Mantieni il contenuto operativo: checklist e criteri, non spiegazioni generiche.
4. Se creata durante un progetto, salvala prima come Knowledge Candidate (`projects/<id>/knowledge-candidates/`), poi promuovila tramite Knowledge Evolution.

**Cosa appartiene a una capability:**
- Pratiche specifiche per una tecnologia o un dominio
- Checklist di cose da verificare o evitare
- Failure mode noti e come rilevarli
- Criteri di sicurezza o performance rilevanti per l'argomento

**Cosa NON appartiene a una capability:**
- Tutorial o introduzioni generiche
- Decisioni che appartengono a un blueprint
- Contesto specifico di un progetto

---

## Come Aggiungere un Archetype

Un archetype è uno scheletro riutilizzabile per generare agenti temporanei di un tipo ricorrente. Definisce ruolo, responsabilità, input, output, confini e Definition of Done. **Non** contiene conoscenza tecnica specifica (quella appartiene alle capability).

**Campi obbligatori** (segui gli archetype esistenti come riferimento):
- Scopo
- Natura dell'archetype
- Responsabilità
- Input attesi
- Output attesi
- Limiti
- Capability compatibili
- Handoff richiesto
- Definition of Done
- Failure mode da evitare

**Passi:**
1. Verifica che il ruolo sia genuinamente ricorrente tra progetti diversi (i ruoli occasionali devono essere agenti ad hoc, non archetype).
2. Crea `archetypes/<ruolo>.md` usando gli archetype esistenti come riferimento di formato.
3. Non includere nell'archetype contesto specifico di progetto o conoscenza tecnica.
4. Se creato durante un progetto, salvalo prima come Knowledge Candidate.

---

## Come Aggiungere un Runtime Adapter

Un runtime adapter definisce le regole di traduzione da un Agent Package generico al formato e al modello di esecuzione di un runtime specifico.

**Sezioni obbligatorie** (segui `runtime-adapters/manual-execution.md` come riferimento):
- Scopo
- Quando si usa
- Prerequisiti
- Come tradurre un Agent Package
- Come gestire gli Handoff
- Come gestire i Human Gate
- Failure mode da evitare

**Passi:**
1. Crea `runtime-adapters/<nome-runtime>.md`.
2. L'adapter non deve contenere logica decisionale della factory — traduce, non decide.
3. Documenta esplicitamente tutti i vincoli e le limitazioni specifici del runtime.
4. Aggiungi il nuovo adapter alla tabella dei runtime adapter in `implementation-status.md`.

---

## Come Aggiornare uno Standard

Gli standard sono contratti di formato. Modificarli impatta tutti gli artefatti esistenti e futuri che vi fanno riferimento.

**Prima di modificare uno standard:**
1. Identifica tutti gli artefatti esistenti che seguono lo standard (cerca in `projects/`, `agents/`, `archetypes/`).
2. Valuta l'impatto — le modifiche incompatibili richiedono la migrazione degli artefatti esistenti.
3. Proponi la modifica come Knowledge Candidate durante un'esecuzione di progetto.
4. Ottieni l'approvazione esplicita tramite l'agente Knowledge Evolution.

**Quando modifichi uno standard:**
1. Aggiorna la tabella dei campi obbligatori/opzionali.
2. Aggiorna l'esempio di formato nello standard.
3. Aggiorna la lista dei failure mode se emergono nuovi anti-pattern.
4. Aggiorna `implementation-status.md`.

---

## Come Aggiungere un Agente Permanente

Gli agenti permanenti sono ruoli di governance nella factory. Aggiungerne uno significa introdurre una nuova responsabilità stabile nel processo centrale della factory.

**Sezioni obbligatorie** (segui gli agenti esistenti come riferimento):
- Identità
- Responsabilità
- Input
- Output
- Limiti
- Workflow
- Definition of Done
- Failure mode da evitare

**Passi:**
1. Verifica che il ruolo non si sovrapponga a un agente permanente esistente.
2. Definisci chiaramente la singola responsabilità dell'agente.
3. Crea `agents/<nome-agente>/<nome-agente>.md`.
4. Aggiorna la tabella degli agenti permanenti in `AgentFactory.md` e `implementation-status.md`.
5. I nuovi agenti permanenti richiedono revisione esplicita — proponi prima come Knowledge Candidate.

---

## Ciclo di Vita della Knowledge Candidate

Quando identifichi un miglioramento durante un progetto:

```text
1. Crea la proposta in projects/<project-id>/knowledge-candidates/
   seguendo standards/knowledge-candidate-standard.md

2. Attiva l'agente Knowledge Evolution per valutarla

3. Se Accettata → Knowledge Evolution la integra nei file permanenti corretti

4. Se Rifiutata → il motivo viene registrato nel file Knowledge Candidate;
                  nessuna modifica permanente

5. Aggiorna lo stato della Knowledge Candidate:
   Proposta → Revisionata → Accettata → Integrata
                           → Rifiutata
```

Non saltare mai questo ciclo. Anche i miglioramenti ovvi devono essere valutati prima di entrare nei file permanenti.

---

## Checklist Prima di Inviare una Modifica

- [ ] La modifica appartiene alla conoscenza permanente (non è specifica di progetto)
- [ ] Il file segue lo standard o il riferimento di formato corretto
- [ ] La nomenclatura segue la convenzione `kebab-case`
- [ ] La lingua è l'italiano (coerente con i documenti esistenti)
- [ ] Nessuna sovrapposizione con agenti permanenti, archetype o capability esistenti
- [ ] `implementation-status.md` aggiornato se è stato aggiunto un nuovo artefatto
- [ ] La modifica è stata proposta come Knowledge Candidate e approvata prima dell'integrazione
