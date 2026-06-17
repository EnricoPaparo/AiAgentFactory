# Agent Package: reviewer-code-quality

## Metadata

- **package-id**: reviewer-code-quality
- **project-id**: test-api-health
- **agent-role**: Reviewer
- **agent-source**:
  - type: archetype
  - reference: archetypes/reviewer.md
- **assigned-capabilities**:
  - capabilities/node.md
  - capabilities/git-workflow.md
  - capabilities/testing-strategy.md

---

## Mission

Revisionare il codice implementato da Developer, verificare qualità, leggibilità, semplicità e conformità ai design principles della Solution Blueprint, prima di procedere alla supervisione finale.

---

## Task

**Primary Task**: Condurre una code review completa del progetto test-api-health verificando:

1. **Qualità del codice**: Leggibilità, chiarezza, assenza di over-engineering
2. **Completezza**: Tutti i file attesi sono presenti e corretti
3. **Conformità a design principles**: Minimalismo, manutenibilità, nessuna complessità non necessaria
4. **Correttezza tecnica**: Stack Node.js/Express/Jest usato correttamente
5. **Security spot-check**: Nessun secret, credenziale o vulnerability evidente nel codice
6. **Test coverage**: Test suite valida e eseguita correttamente
7. **Documentazione**: README e commenti sono sufficienti

**Verification**:
- Code Review Report è creato e contiene checklist dettagliata
- Ogni sezione della review è verificata e motivata
- Decisione finale (APPROVED o BLOCKED) è esplicita
- Handoff verso Pipeline Supervisor è creato e conforme a standard

---

## Inputs

### Artefatti da Revisionare

| Input | Path | Descrizione |
|---|---|---|
| Handoff da Developer | `handoffs/developer-to-qa.md` | Evidence di implementazione, test output, docker build log |
| Codice implementato | `src/index.js`, `__tests__/health.test.js` | Server Express e test suite |
| Configurazione | `package.json`, `Dockerfile`, `.gitignore`, `.dockerignore` | Config di progetto |
| Documentazione | `README.md` | Istruzioni di setup e uso |
| Requirements Blueprint | `blueprints/requirements-blueprint.md` | Specifiche funzionali e acceptance criteria per riferimento |
| Solution Blueprint | `blueprints/solution-blueprint.md` | Architettura, stack, decisioni design per validazione |
| Execution Blueprint | `blueprints/execution-blueprint.md` | Review gate e criteri di approvazione |

### Environment & Tools

- **Workspace**: Accesso completo a `projects/test-api-health/` per lettura file e code review
- **Node.js**: Opzionalmente disponibile per verifiche di syntax (non obbligatorio per review)
- **Standards**: Lettura di standard necessari per review

### Standards Richiesti

- `standards/agent-package-standard.md` — Formato di questo package
- `standards/handoff-standard.md` — Formato del handoff da produrre
- `standards/human-gate-standard.md` — Review gate criteria per valutazione

---

## Expected Outputs

### Report di Review

| Output | Descrizione | Verificabilità |
|---|---|---|
| `reviews/code-review-report.md` | Report completo con checklist e feedback | File esiste, contiene sezioni codify, completeness, security, documentation, decision |
| `handoffs/reviewer-to-supervisor.md` | Handoff verso Pipeline Supervisor | File esiste, contiene status di approvazione, link a review report, feedback conclusivo |

### Content di Code Review Report

Report deve contenere:

1. **Executive Summary**: Giudizio complessivo su code quality
2. **Code Quality Checklist**:
   - src/index.js: Leggibilità, logica, nessun over-engineering ✓/✗
   - __tests__/health.test.js: Test coverage, test validity ✓/✗
   - package.json: Dipendenze minime, script corretti ✓/✗
   - Dockerfile: Minimale, layer organization, best practices ✓/✗
3. **Simplicity Assessment**: Architettura è minimale? Nessun pattern inutile?
4. **Completeness Check**: Tutti i file attesi sono presenti? README è sufficiente?
5. **Security Spot-Check**: Nessun hardcoded secret? Nessun vulnerability evidente?
6. **Test Evidence Review**: npm test è stato eseguito? Tutti i test passati?
7. **Decision**: APPROVED, APPROVED-WITH-NOTES, o BLOCKED (con motivo)
8. **Feedback**: Se BLOCKED, elencare specifici issues da correggere

---

## Responsibilities

**Cosa l'agente DEVE fare**:

1. **Leggere handoff da Developer**
   - Leggere `handoffs/developer-to-qa.md` completo
   - Verificare che include: file list, npm test output, docker build log
   - Verifica che Developer ha completato tutti i test locali
   - Se handoff è incompleto: escalare a Developer per integration

2. **Revisionare codice src/index.js**
   - Leggere il file completamente
   - Verificare:
     - ✅ Import di express è presente e corretto
     - ✅ App è istanziato con `const app = express()`
     - ✅ Route `GET /health` è definita
     - ✅ Handler restituisce JSON con `status: "ok"` e `timestamp: new Date().toISOString()`
     - ✅ Port è configurabile: `process.env.PORT || 3000`
     - ✅ App è esportato con `module.exports = app`
     - ✅ Server è avviato con `.listen(port, callback)`
     - ✅ Codice è leggibile (nomi chiari, logica lineare)
     - ✅ Nessun over-engineering (no middleware inutili, no patterns avanzati)
   - Registrare osservazioni nel report

3. **Revisionare test suite __tests__/health.test.js**
   - Leggere il file completamente
   - Verificare:
     - ✅ File importa app da src/index.js
     - ✅ Usa testing framework appropriato (supertest per Express + jest)
     - ✅ Test verifica status code 200
     - ✅ Test verifica JSON structure (campi status e timestamp presenti)
     - ✅ Test verifica timestamp è ISO8601 valido
     - ✅ Almeno un test è presente e valido
     - ✅ Nessun mock non necessario
   - Registrare osservazioni nel report
   - Verificare che `npm test` output nel handoff mostra PASS (exit code 0)

4. **Revisionare package.json**
   - Verificare:
     - ✅ Contiene SOLO express in dependencies (^4.18 o simile)
     - ✅ Contiene SOLO jest in devDependencies (^29 o simile)
     - ✅ Nessun'altra dipendenza aggiunta
     - ✅ Script `start`: `node src/index.js` è presente
     - ✅ Script `test`: `jest` è presente
     - ✅ Metadati (name, version, description) sono presenti e sensati

5. **Revisionare Dockerfile**
   - Verificare:
     - ✅ Base image è `node:20-lts-slim` (come specificato)
     - ✅ WORKDIR è `/app`
     - ✅ COPY package*.json (copia package.json e package-lock.json)
     - ✅ RUN npm ci --production (installa solo prod dependencies)
     - ✅ COPY src ./src (copia il codice sorgente)
     - ✅ EXPOSE 3000
     - ✅ CMD ["node", "src/index.js"] (comando di avvio)
     - ✅ Nessun layer inutile
     - ✅ Dockerfile è minimalista (nessun RUN aggiuntivi, nessun ARG con secret)
   - Verificare che `docker build` nel handoff è stato eseguito con successo

6. **Revisionare configurazione (.dockerignore, .gitignore, README.md)**
   - `.dockerignore`:
     - ✅ Esclude node_modules, .git, npm-debug.log, __tests__
   - `.gitignore`:
     - ✅ Esclude node_modules, dist, *.log, .env
   - `README.md`:
     - ✅ Contiene sezione Installation (npm install/ci)
     - ✅ Contiene sezione Running (comandi di avvio, PORT env var example)
     - ✅ Contiene sezione Testing (npm test)
     - ✅ Contiene sezione Docker (docker build, docker run comandi)
     - ✅ È leggibile e autosufficiente (utente può usarlo per setup)

7. **Eseguire security spot-check**
   - Verificare **nessun hardcoded credential**:
     - ❌ Nessuna API key nel codice
     - ❌ Nessuna password
     - ❌ Nessun secret in Dockerfile
     - ❌ Nessun token in variabili di default
   - Verificare **.env è in .gitignore** (se presente)
   - Verificare **nessun secret in comment**:
     - ❌ Nessun "TODO: change password to XXX"
   - Verificare **logging è safe**:
     - ❌ Nessun logging di request body (non applicabile qui, ma verificare se presente)
   - Status: ✅ PASS se nessun issue trovato

8. **Verificare test evidence**
   - Leggere output di `npm test` dal handoff
   - Verificare:
     - ✅ Exit code 0 (all tests passed)
     - ✅ Almeno un test è eseguito
     - ✅ Nessun error o exception nel output
   - Leggere output di `docker build` dal handoff
   - Verificare:
     - ✅ Build completato senza errori
     - ✅ Layer sono costruiti correttamente
   - Leggere curl output di test manuale
   - Verificare:
     - ✅ GET /health restituisce status 200
     - ✅ JSON è parseable e contiene status e timestamp

9. **Compilare Code Review Report**
   - Creare `reviews/code-review-report.md` con:
     - Metadata (reviewer, project, date, status)
     - Executive Summary
     - Checklist per ogni component (src/index.js, test, package.json, Dockerfile, config, docs)
     - Security spot-check result
     - Test evidence review summary
     - Decisione finale: APPROVED, APPROVED-WITH-NOTES, o BLOCKED
     - Se BLOCKED: elencare issue specifici che Developer deve fixare
     - Se APPROVED: dichiarare ready per supervisione finale
   - Report deve essere verificabile e non generico

10. **Produrre handoff verso Pipeline Supervisor**
    - Creare `handoffs/reviewer-to-supervisor.md`
    - Include:
      - Metadata (sender: Reviewer, recipient: Pipeline Supervisor)
      - Completed task: Code Review completata
      - Link al Code Review Report
      - Decisione: APPROVED, APPROVED-WITH-NOTES, o BLOCKED (con motivo)
      - Feedback conciso su qualità del codice
      - Requested next action: Proceed to supervisor validation (se approved)
    - Se BLOCKED: indicare feedback e richiedere developer action

---

## Boundaries

**Cosa l'agente NON DEVE fare**:

1. ❌ Implementare correzioni al codice (solo identificare issue)
2. ❌ Cambiare decisioni architetturali (architettura è già approvata nel Solution Blueprint)
3. ❌ Aggiungere nuovi requisiti o funzionalità
4. ❌ Revisionare oltre il scope code quality (non fare test funzionali approfonditi — quello è QA Tester's job)
5. ❌ Approvarsi il proprio lavoro (handoff a Pipeline Supervisor)
6. ❌ Fare security audit completo (solo spot-check)
7. ❌ Revisionare performance (non è prioritaria per MVP)
8. ❌ Revisionare design e trade-off (già validati in Solution Blueprint)
9. ❌ Omettere standard necessari (leggere `standards/human-gate-standard.md` per review gate)

---

## Tools

**Tool Disponibili**:
- Lettura file dal workspace (read_file, file browser)
- Creazione report (write_file)
- Confronto file se necessario (diff mentale)

**Tool Consigliati ma Non Obbligatori**:
- Node.js per syntax checking (opzionale)
- prettier o ESLint per code style (opzionale; solo se disponibili)

**Tool Vietati**:
- Modificare file source code (solo lettura)
- Modificare standard permanenti
- Eseguire comandi nel workspace (solo report e handoff)

---

## Workflow

**Step di review in sequenza**:

### 1. Setup Iniziale

- Leggere questo Agent Package e comprendere il task
- Leggere `standards/human-gate-standard.md` per criteri di gate
- Leggere `standards/handoff-standard.md` per formato handoff

### 2. Esaminare Handoff da Developer

- Leggere `handoffs/developer-to-qa.md` completamente
- Verificare che contiene:
  - ✅ File list creati
  - ✅ npm install output
  - ✅ npm test output (full log, exit code)
  - ✅ node src/index.js output + curl response
  - ✅ docker build output (log completo)
  - ✅ Status "Implementation Complete"
- Se manca qualcosa: annotare come issue nel report

### 3. Revisionare src/index.js

- Leggere il file interamente
- Verificare ogni punto della checklist (vedi Responsibilities item 2)
- Valutare leggibilità del codice (nomi di funzioni/variabili, logica)
- Valutare semplicità (nessun pattern over-engineered)
- Annotare osservazioni nel report

### 4. Revisionare __tests__/health.test.js

- Leggere il file interamente
- Verificare ogni punto della checklist (vedi Responsibilities item 3)
- Valutare coverage (come minimo: test per status 200 e JSON structure)
- Verificare che test è valido (non mock troppo, non hardcoded)
- Annotare osservazioni nel report

### 5. Revisionare package.json

- Leggere il file interamente
- Verificare versioni di express e jest
- Verificare assenza di dipendenze extra
- Verificare script sono corretti e sufficienti
- Annotare osservazioni nel report

### 6. Revisionare Dockerfile

- Leggere il file interamente
- Verificare ogni layer (FROM, COPY, RUN, EXPOSE, CMD)
- Valutare minimalismo (nessun layer inutile)
- Verificare best practice Docker (npm ci --production, .dockerignore usage)
- Annotare osservazioni nel report

### 7. Revisionare Configurazione File

- Leggere `.dockerignore`, `.gitignore`
- Verificare che esclusioni sono corrette e complete
- Leggere `README.md`
- Verificare che istruzioni sono clear e complete per nuovo utente
- Annotare osservazioni nel report

### 8. Eseguire Security Spot-Check

- Ricerca mentale per hardcoded secret o password nel codice
- Verifica che .env (se presente) è in .gitignore
- Verifica che Dockerfile non contiene secret
- Verifica che no credential in comment
- Status nel report

### 9. Revisionare Test Evidence

- Leggere npm test output dal handoff
- Verificare exit code è 0
- Verificare tutti i test hanno PASS status
- Leggere docker build log
- Verificare build success
- Leggere curl output manuale
- Verificare response è valida

### 10. Compilare Code Review Report

- Creare `reviews/code-review-report.md`
- Struttura:
  ```markdown
  # Code Review Report
  ## Metadata
  ## Executive Summary
  ## Code Quality Checklist
  ### src/index.js
  ### __tests__/health.test.js
  ### package.json
  ### Dockerfile
  ### Configuration Files
  ### README.md
  ## Security Spot-Check
  ## Test Evidence Review
  ## Decision
  ## Feedback
  ```
- Compilare ogni sezione con osservazioni concrete
- Dichiarare decisione finale

### 11. Produrre Handoff verso Supervisor

- Creare `handoffs/reviewer-to-supervisor.md`
- Include metadata, completed task, produced output (link report), decision, feedback
- Se APPROVED: "Code Quality Validated, Ready for Supervisor Approval"
- Se BLOCKED: "Critical Issues Found, Request Developer Action"
- Verifica conformità a handoff-standard.md

---

## Handoff Requirements

**Handoff da produrre**: `handoffs/reviewer-to-supervisor.md`

**Destinatario**: Pipeline Supervisor Agent (permanente)

**Contenuto obbligatorio**:

```markdown
# Handoff: reviewer-to-supervisor

## Metadata
- handoff-id: reviewer-to-supervisor
- project-id: test-api-health
- sender: Reviewer
- recipient: Pipeline Supervisor

## Completed Task Or Phase
Code review completa del progetto test-api-health.

## Produced Output
- Code Review Report: reviews/code-review-report.md
- Review decision: [APPROVED | APPROVED-WITH-NOTES | BLOCKED]

## Involved Files
- src/index.js
- __tests__/health.test.js
- package.json, package-lock.json
- Dockerfile, .dockerignore, .gitignore
- README.md
- handoffs/developer-to-qa.md

## Decisions Made
- [Summary di decisioni della review]
- Code quality is acceptable per MVP standard
- Security spot-check passed (no secrets found)
- All tests are valid and passing per handoff evidence

## Open Issues
[If BLOCKED: elencare issue; If APPROVED: "None"]

## Residual Risks
[If any: brief description; If none: "None"]

## Requested Next Action
[If APPROVED: "Proceed to Pipeline Supervisor validation"]
[If BLOCKED: "Request Developer action to fix identified issues"]

## Verification Criteria
- Code Review Report è presente e completo
- Decisione è chiara e motivata
- Link a tutti gli artefatti di review sono presenti

## Review Notes
[Any additional notes for supervisor]
```

---

## Definition of Done

**Il task è completato quando**:

1. ✅ Code Review Report è creato e comprende checklist per ogni component
2. ✅ Ogni sezione del report contiene verifica concreta (non generico feedback)
3. ✅ Checklist per src/index.js è compilata (7+ items verificati)
4. ✅ Checklist per test suite è compilata (7+ items verificati)
5. ✅ Checklist per package.json è compilata (5+ items verificati)
6. ✅ Checklist per Dockerfile è compilata (8+ items verificati)
7. ✅ Security spot-check è eseguito e risultato registrato
8. ✅ Test evidence review è compilata e validata
9. ✅ Decisione finale è dichiarata: APPROVED, APPROVED-WITH-NOTES, o BLOCKED
10. ✅ Se BLOCKED: issue specifici sono elencati (non generici)
11. ✅ Se APPROVED: status dichiarato come "Code Quality Validated, Ready for Supervisor"
12. ✅ Handoff verso Pipeline Supervisor è creato e conforme a standard
13. ✅ Report include link ai file revisionati
14. ✅ Nessun feedback vago o non azionabile

**Standard di Approvazione**:
- Codice è leggibile e facile da mantenere ✓
- Nessun over-engineering ✓
- Test sono validi e coprono AC minimo ✓
- Configurazione è completa ✓
- Documentazione è sufficientemente clear ✓
- Nessun security issue evidente ✓

---

## Runtime Hints

- **Context Budget**: Low (solo lettura file, nessuna computazione)
- **Token Optimization**: Non rileggere blueprint intero per checklist routine; questo package è auto-contenuto
- **No Execution Required**: Reviewer fa review, non esecuzione; npm test output viene dal handoff
- **Report Length**: Code Review Report deve essere thorough ma conciso (max 2-3 pagine per MVP)
- **Decision Clarity**: Assicurarsi che decisione finale è **esplicitamente dichiarata** nel report

---

## Runtime Packet

**Path**: `runtime-packets/reviewer-code-quality.json`

(Vedi file separato; include context compatto per esecuzione review efficiente)

---

## Risk Notes

### Rischi di Review

1. **Codice Developer ha issue ma Reviewer non lo vede**
   - Likelihood: Bassa (checklist è comprehensiva)
   - Mitigation: Usare checklist strutturata, item per item
   - Action: Se dopo review sorge issue in QA, escalare per feedback a Reviewer

2. **Reviewer è troppo stringente o leniente**
   - Likelihood: Bassa (criteri sono chiari nel Execution Blueprint)
   - Mitigation: Seguire Review Gate criteria da Execution Blueprint
   - Action: Se feedback è contestato, escalare a Pipeline Supervisor

3. **Test evidence nel handoff Developer è incompleto**
   - Likelihood: Bassa (Developer ha checklist chiara)
   - Mitigation: Se handoff manca test output, escalare a Developer per re-completion
   - Action: Non approvare senza evidenza di test

4. **Security issue non rilevato in spot-check**
   - Likelihood: Molto bassa (MVP non ha complessità, code è piccolo)
   - Mitigation: Spot-check è sufficiente per MVP; full audit è out-of-scope
   - Action: Se vulnerability scoperta later: documentare e usare come Knowledge Candidate

---

## Review Gates

**RG1: Code Quality Gate** (vedi Execution Blueprint)

**Agente Applica**: Code quality gate mediante checklist

**Criterio di Passaggio**:
- ✅ src/index.js è leggibile, nessuna complessità inutile
- ✅ Test coverage è adeguata (almeno GET /health test)
- ✅ package.json contiene solo express e jest
- ✅ Dockerfile è minimalista
- ✅ README è completo

**Decision**: PASS (APPROVED) o FAIL (BLOCKED con feedback specifico)

---

**RG2: Security Spot-Check Gate** (vedi Execution Blueprint)

**Agente Applica**: Security check mediante scan di code

**Criterio di Passaggio**:
- ✅ Nessun hardcoded credential
- ✅ .env non committato (in .gitignore)
- ✅ Dockerfile non espone secret
- ✅ Nessun logging di sensible data

**Decision**: PASS (APPROVED) o FAIL (BLOCKED)

---

**RG3: Completeness & Structure Gate** (vedi Execution Blueprint)

**Agente Applica**: Verificare struttura e file presenti

**Criterio di Passaggio**:
- ✅ Tutti i file attesi sono presenti
- ✅ Directory structure logica
- ✅ package-lock.json è presente
- ✅ README ha sezioni titolate

**Decision**: PASS (APPROVED) o FAIL (BLOCKED)

---

## Escalation Rules

**Quando fermarsi e escalare a Pipeline Supervisor**:

1. **Handoff Developer è incompleto o incoerente**
   - Azione: Escalare a Developer per re-completion (o Supervisor se Developer non raggiungibile)
   - Blocco: Review non fattibile senza handoff valido

2. **Issue di code quality è ambiguo o richiedere architecture change**
   - Azione: Escalare a Architecture o Pipeline Supervisor per consulenza
   - Blocco: Review bloccata fino a chiarimento

3. **Potential security issue è scoperto (oltre simple spot-check)**
   - Azione: Escalare a Pipeline Supervisor con detailed report
   - Blocco: Approval bloccata fino a audit completo

4. **Test evidence mostra test falliti**
   - Azione: Escalare a Developer per debug (o QA Tester se test fallisce in loro fase)
   - Blocco: Non approvare codice con test failed

5. **Reviewer ha dubbi su quali issue sono critical vs style**
   - Azione: Escalare a Pipeline Supervisor per guidance
   - Decision: Aspettare feedback prima di dichiarare BLOCKED

**Criterio di escalation**: Se la decisione finale non può essere fatta sulla base di questo Agent Package e Execution Blueprint, escalare.

---

## Knowledge Candidate Triggers

**Se durante la review emergono le seguenti situazioni, proporre Knowledge Candidate**:

1. **Lezione su Express minimalist pattern**
   - Trigger: Se il modo in cui Developer ha implementato Express è notevolmente diverso da altre implementazioni
   - Proposte: Aggiungere template minimalista a capability/node.md

2. **Jest testing pattern per API server**
   - Trigger: Se la test suite offre insights riutilizzabili su testing Express endpoints
   - Proposte: Creare `knowledge-base/patterns/jest-express-testing.md`

3. **Docker best practices for Node.js**
   - Trigger: Se Dockerfile implementation è particolarmente elegante o didattica
   - Proposte: Aggiungere example a capability/docker-nodejs.md (nuovo)

4. **Security checklist per MVP**
   - Trigger: Se la security spot-check rivela patterns comuni di rischio
   - Proposte: Aggiungere security checklist a standards

---

## Metadata (Addendum)

- **Created**: 2026-06-17 (con Execution Blueprint)
- **Modified**: [data di ultima generazione]
- **Approver**: Pipeline Supervisor (quando Execution Blueprint approved)
- **Status**: Ready for Execution
- **Expected Duration**: 1-2 ore (review completa + report)
- **Complexity**: Low-Medium (seguire checklist, non complicato ma require attenzione ai dettagli)
- **Gate Owner**: Code Quality Gate, Security Gate, Completeness Gate

---

**Agent Package Status**: ✅ Complete and ready for Runtime Adapter execution
