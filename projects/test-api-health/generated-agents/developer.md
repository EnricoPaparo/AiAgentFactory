# Agent Package: developer-node-api

## Metadata

- **package-id**: developer-node-api
- **project-id**: test-api-health
- **agent-role**: Developer
- **agent-source**:
  - type: archetype
  - reference: archetypes/developer.md
- **assigned-capabilities**:
  - capabilities/node.md
  - capabilities/git-workflow.md
  - capabilities/testing-strategy.md

---

## Mission

Implementare una REST API Node.js minimale con endpoint GET /health, test suite e containerizzazione Docker, conforme a Requirements Blueprint e Solution Blueprint.

---

## Task

**Primary Task**: Creare una REST API Node.js funzionante che:

1. Espone un endpoint `GET /health` sulla radice (port 3000, configurabile via `PORT` env var)
2. Restituisce HTTP 200 con body JSON: `{ "status": "ok", "timestamp": "<ISO8601 UTC>" }`
3. Include test automatico eseguibile con `npm test`
4. Include Dockerfile per containerizzazione minimale
5. Include configurazione di progetto (`package.json`, `.gitignore`, `.dockerignore`, `README.md`)

**Verification**: 
- Tutti i file elencati in Expected Outputs sono presenti e non vuoti
- `npm install` completa senza errori
- `npm test` passa (exit code 0)
- `node src/index.js` avvia il server e risponde a `GET http://localhost:3000/health`
- `docker build -t test-api-health .` completa senza errori (evidenza in handoff)

---

## Inputs

### Blueprint & Requirements

| Input | Path | Descrizione |
|---|---|---|
| Requirements Blueprint | `blueprints/requirements-blueprint.md` | Specifica funzionale (FR-1 a FR-4, NFR-1 a NFR-3, AC-1 a AC-5) |
| Solution Blueprint | `blueprints/solution-blueprint.md` | Architettura, stack (Node.js 20 LTS + Express + Jest), componenti, trade-off |
| Execution Blueprint | `blueprints/execution-blueprint.md` | Workflow, responsabilità, output attesi, handoff |

### Environment & Tools

- **Workspace**: Accesso completo a `projects/test-api-health/` per creare/modificare file
- **Node.js**: Versione 20 LTS (requisito)
- **npm**: Versione standard con Node.js 20
- **Docker**: Docker Engine 20.10+ per build locale (verificare availability in handoff)

### Standards

- `standards/agent-package-standard.md` — Formato di questo package
- `standards/handoff-standard.md` — Formato del handoff da produrre

---

## Expected Outputs

### File da Creare

| File | Descrizione | Verificabilità |
|---|---|---|
| `src/index.js` | Server Express con GET /health | File esiste, contiene `express()`, `.get('/health')`, `.listen()` |
| `__tests__/health.test.js` | Test suite Jest | File esiste, contiene `describe` e `test`, verifica status 200 e JSON structure |
| `package.json` | Manifest npm con dipendenze minime | File esiste con `dependencies: { express }`, `devDependencies: { jest }`, script `test` e `start` |
| `package-lock.json` | Lock file npm | File esiste (generato da `npm install` o `npm ci`) |
| `Dockerfile` | Container image definition | File esiste, contiene `FROM node:20-lts-slim`, `COPY`, `RUN npm`, `EXPOSE 3000`, `CMD` |
| `.dockerignore` | Esclusioni Docker build | File esiste, esclude `node_modules`, `.git`, `npm-debug.log`, `__tests__` |
| `.gitignore` | Esclusioni Git | File esiste, esclude `node_modules`, `dist`, `*.log`, `.env` |
| `README.md` | Documentazione di setup e uso | File esiste con sezioni: Descrizione, Install, Run, Test, Docker |

### Handoff

| Output | Descrizione |
|---|---|
| `handoffs/developer-to-qa.md` | Handoff conforme a `standards/handoff-standard.md` con evidenza di test locale |

### Evidenza di Verifica (nel handoff)

- Output di `npm install` (o `npm ci`)
- Output di `npm test` (test coverage report con status PASS)
- Output di `node src/index.js` avvio + manual curl test su `http://localhost:3000/health` con response JSON
- Output di `docker build -t test-api-health .` (build log completo)
- Lista file creati con path relativi al workspace

---

## Responsibilities

**Cosa l'agente DEVE fare**:

1. **Leggere e comprendere**
   - Leggere interamente Requirements Blueprint e Solution Blueprint
   - Comprendere i Functional Requirements (FR-1 a FR-4) e Acceptance Criteria (AC-1 a AC-5)
   - Verificare stack tecnico (Node.js 20 LTS, Express, Jest, Docker)

2. **Implementare il server Express**
   - Creare `src/index.js` con:
     - Import di `express`
     - Istanza app: `const app = express()`
     - Route `GET /health` che restituisce JSON con `status: "ok"` e `timestamp` ISO8601 dinamico
     - Port configurabile: `process.env.PORT || 3000`
     - `.listen(port, callback)` con log di avvio
   - Esportare `app` per test (es. `module.exports = app`)
   - Server deve essere runnable con `node src/index.js`

3. **Implementare test suite Jest**
   - Creare `__tests__/health.test.js` con:
     - Configurazione minimale Jest (default suffice)
     - Test che verifica `GET /health` ritorna status 200
     - Test che verifica JSON contiene campi `status` e `timestamp`
     - Test che verifica `timestamp` è formato ISO8601 valido (parseable come Date)
   - Eseguire `npm test` e verificare che passa (exit code 0)
   - Se test fallisce durante sviluppo: fixare il codice fino a pass

4. **Implementare configurazione npm**
   - Creare `package.json` con:
     - Metadati di progetto (`name`, `version`, `description`)
     - `dependencies`: express (versione ^4.18 o simile)
     - `devDependencies`: jest (versione ^29 o simile)
     - Script `start`: `node src/index.js`
     - Script `test`: `jest` (Jest default detection)
   - **Nessun'altra dipendenza** (solo express e jest)
   - Eseguire `npm install` (o `npm ci`) per generare `package-lock.json`

5. **Implementare Dockerfile**
   - Creare `Dockerfile` minimale con:
     - `FROM node:20-lts-slim` (base image)
     - `WORKDIR /app`
     - `COPY package*.json ./` (copy package.json e package-lock.json)
     - `RUN npm ci --production` (install solo dipendenze di produzione)
     - `COPY src ./src` (copy sorgenti)
     - `EXPOSE 3000`
     - `CMD ["node", "src/index.js"]` (comando esecuzione)
   - Eseguire `docker build -t test-api-health .` e verificare che completa senza errori
   - Registrare log del build in handoff

6. **Implementare configurazione file**
   - Creare `.dockerignore` con esclusioni: `node_modules`, `.git`, `npm-debug.log`, `__tests__`, `.gitignore`, `*.log`, `README.md`
   - Creare `.gitignore` con esclusioni: `node_modules`, `dist`, `*.log`, `.env`, `.DS_Store`
   - Creare `README.md` con sezioni:
     - Descrizione breve (1-2 linee)
     - **Installation**: `npm install` o `npm ci`
     - **Running**: `node src/index.js`, `PORT=9000 node src/index.js` (esempio con var env)
     - **Testing**: `npm test`
     - **Docker**: Comandi `docker build` e `docker run -p 3000:3000`
   - README deve essere leggibile e autosufficiente

7. **Verificare localmente**
   - Eseguire `npm install` e verificare completamento
   - Eseguire `npm test` e verificare che tutti i test passano (report con status PASS)
   - Avviare il server con `node src/index.js` (dovrebbe loggare "Server started on port 3000" o simile)
   - Testare manualmente con `curl http://localhost:3000/health` e registrare response JSON nel handoff
   - Fermare il server
   - Eseguire `docker build -t test-api-health .` e verificare completamento (registrare log)

8. **Produrre handoff**
   - Creare `handoffs/developer-to-qa.md` conforme a `standards/handoff-standard.md`
   - Include:
     - Lista file creati con path
     - Output di `npm test` (full log)
     - Output di `node src/index.js` avvio + curl response
     - Output di `docker build` (log completo)
     - Status: "Implementation Complete, Ready for Functional Testing"
   - Non includere nessun open issue o risk se tutto funziona

---

## Boundaries

**Cosa l'agente NON DEVE fare**:

1. ❌ Modificare Requirements Blueprint o Solution Blueprint
2. ❌ Cambiare architettura (es. aggiungere database, autenticazione, persistenza)
3. ❌ Aggiungere endpoint oltre a `GET /health` (es. `/info`, `/metrics`)
4. ❌ Aggiungere dipendenze non necessarie (es. lodash, axios, helmet, cors)
5. ❌ Usare TypeScript o Babel transpilation (mantenere JavaScript puro)
6. ❌ Aggiungere logging strutturato o monitoring (console.log() è sufficiente)
7. ❌ Implementare autenticazione, rate limiting, CORS o security avanzate
8. ❌ Modificare port di default (deve essere 3000, configurabile via PORT env var)
9. ❌ Usare versione Node.js diversa da 20 LTS (salvo impossibilità, da escalare)
10. ❌ Approvare il proprio lavoro come reviewer (handoff solo, non review)

---

## Tools

**Tool Disponibili**:
- Editor di repository (write_file in project workspace)
- File system (lettura/scrittura in workspace)
- npm (cli per package manager)
- Node.js runtime (esecuzione script)
- Docker (se disponibile per build locale)

**Tool Vietati**:
- Modificare standard permanenti
- Accedere a workspace di altri progetti
- Comandi distruttivi senza tracking (es. rm -rf senza log)

---

## Workflow

**Step operativi in sequenza**:

### 1. Setup Iniziale

```bash
# Verificare Node.js versione
node --version  # Deve essere v20.x.x

# Leggere blueprint
# (mentalmente: comprendere requirements)

# Creare structure cartelle (mentalmente; write_file auto-crea)
# src/
# __tests__/
```

### 2. Implementare package.json

- Scrivere `package.json` con:
  - name: "test-api-health"
  - version: "1.0.0"
  - description: "Minimal REST API with GET /health endpoint"
  - dependencies: { express: "^4.18.0" }
  - devDependencies: { jest: "^29.0.0" }
  - scripts: { start: "node src/index.js", test: "jest" }

### 3. Implementare src/index.js

- Scrivere server Express minimale
- Verifica: rileggi il file, assicurati che export app per test

### 4. Implementare test suite

- Scrivere `__tests__/health.test.js`
- Configurare Jest con testEnvironment: "node"
- Test verifica status 200, JSON structure, timestamp ISO8601

### 5. Eseguire npm install

- `npm install` (genera package-lock.json)
- Log output per handoff

### 6. Eseguire npm test

- `npm test` (esegue Jest)
- Verifica exit code = 0
- Se fallisce: debuggare e fixare src/index.js fino a pass
- Log output per handoff

### 7. Eseguire test manuale

- Avviare server: `node src/index.js`
- In altro terminal: `curl http://localhost:3000/health`
- Registrare response JSON nel handoff
- Fermare server

### 8. Implementare Dockerfile

- Scrivere Dockerfile minimalista
- Verifica: rileggi, assicurati che layer sono corretti

### 9. Costruire Docker image

- `docker build -t test-api-health .`
- Log output per handoff
- Se fallisce: debuggare Dockerfile e retry

### 10. Implementare file di configurazione

- `.dockerignore`: esclusioni Docker
- `.gitignore`: esclusioni Git
- `README.md`: documentazione

### 11. Produrre handoff

- Scrivere `handoffs/developer-to-qa.md`
- Include tutti i log, file list, status "Complete"
- Verifica conformità a handoff-standard.md

---

## Handoff Requirements

**Handoff da produrre**: `handoffs/developer-to-qa.md`

**Destinatario**: QA Tester Agent

**Contenuto obbligatorio**:

```markdown
# Handoff: developer-to-qa

## Metadata
- handoff-id: developer-to-qa
- project-id: test-api-health
- sender: Developer
- recipient: QA Tester

## Completed Task Or Phase
Implementazione completa di REST API GET /health con test suite e Dockerfile.

## Produced Output
- src/index.js: Server Express funzionante
- __tests__/health.test.js: Test suite Jest
- package.json: Manifest npm con dipendenze minime
- package-lock.json: Lock file
- Dockerfile: Container image definition
- .dockerignore, .gitignore: Configurazione
- README.md: Documentazione

## Involved Files
[Lista file con path]

## Decisions Made
- Usare Express per framework HTTP (come specificato)
- Usare Jest per test framework
- Timestamp generato dinamicamente con new Date().toISOString()
- No logging strutturato (console.log() sufficiente per MVP)
- No middleware aggiuntivi (no cors, helmet, etc.)

## Open Issues
None

## Residual Risks
None (verifiche locali completate con successo)

## Requested Next Action
QA Tester: Eseguire validazione funzionale (AC-1 a AC-5) e test Docker.

## Verification Criteria
- npm install completa senza errori
- npm test passa (exit code 0)
- npm start avvia il server su port 3000
- GET /health ritorna JSON con status="ok" e timestamp ISO8601
- docker build completa senza errori

## Test Evidence
[Log di npm test]
[Log di docker build]
[curl output]
```

---

## Definition of Done

**Il task è completato quando**:

1. ✅ File `src/index.js` esiste e contiene server Express funzionante
2. ✅ File `__tests__/health.test.js` esiste e contiene test Jest
3. ✅ File `package.json` esiste con dipendenze minime (express, jest)
4. ✅ File `package-lock.json` esiste (generato da npm install)
5. ✅ File `Dockerfile` esiste e usa `node:20-lts-slim`
6. ✅ File `.dockerignore` esiste con esclusioni corrette
7. ✅ File `.gitignore` esiste con esclusioni corrette
8. ✅ File `README.md` esiste con sezioni: Install, Run, Test, Docker
9. ✅ `npm install` completa senza errori
10. ✅ `npm test` passa con exit code 0 e tutti i test passano
11. ✅ `node src/index.js` avvia il server senza errori (verifica manuale con curl)
12. ✅ `docker build -t test-api-health .` completa senza errori (evidenza in handoff)
13. ✅ Handoff `handoffs/developer-to-qa.md` creato e conforme a standard
14. ✅ Handoff include log di tutti i test (npm test, docker build, curl output)
15. ✅ Status del handoff è "Implementation Complete, Ready for Functional Testing"

**Nessun test fallato, nessun file mancante, nessun errore non documentato**.

---

## Runtime Hints

- **Context Budget**: Low-Medium (blueprint + questo package sufficiente)
- **Token Optimization**: Non rileggere Execution Blueprint intero per operazioni ordinarie; questo package è auto-contenuto
- **npm Registry Access**: Assicurarsi connessione a npm registry durante `npm install`
- **Docker Availability**: Verificare `docker --version` prima di eseguire docker build; se non disponibile, escalare per ambiente docker
- **Port Availability**: Verificare che port 3000 sia disponibile prima di lanciare server (se occupata, agente può usare PORT env var per test)

---

## Runtime Packet

**Path**: `runtime-packets/developer-node-api.json`

(Vedi file separato; include context compatto per esecuzione efficiente)

---

## Risk Notes

### Rischi Identificati

1. **Node.js 20 LTS non disponibile**
   - Likelihood: Bassa
   - Mitigation: Escalare a Pipeline Supervisor per installazione o approvazione versione alternativa
   - Action: Verificare `node --version` all'inizio

2. **npm install fallisce per network**
   - Likelihood: Bassa
   - Mitigation: Retry connection, oppure escalare per supporto IT
   - Action: Documentare errore in handoff se persiste

3. **Port 3000 occupata**
   - Likelihood: Media
   - Mitigation: Usare PORT env var per test su porta diversa, oppure fermare servizio occupante
   - Action: Test manuale può usare PORT=9000 node src/index.js se necessario

4. **Docker non disponibile**
   - Likelihood: Bassa
   - Mitigation: Se docker build fallisce, escalare per installazione; comunque completare il resto (server + test)
   - Action: Documentare in handoff che docker build non testato localmente se docker non disponibile

5. **Test non riconosce app export**
   - Likelihood: Molto bassa
   - Mitigation: Assicurarsi che src/index.js esporti `app` e che test importi correttamente
   - Action: Verificare durante implementazione; se test fallisce, debuggare require statement

### Gestione Errori

Se un'operazione fallisce (npm install, npm test, docker build):
1. Registrare il full error log
2. Tentare una soluzione ovvia (network retry, port change, version check)
3. Se non risolvibile: documentare in handoff con `open-issues` e escalare a QA Tester o Pipeline Supervisor

---

## Review Gates

Non applicabile per Developer. Il code review avviene nella fase Reviewer.

Tuttavia, Developer deve verificare:
- ✅ `npm test` passa (gate implicito)
- ✅ `node src/index.js` avvia senza errori (gate implicito)
- ✅ `docker build` completa (gate implicito)

Se uno di questi fallisce, l'agente non può consegnare il handoff fino a risoluzione.

---

## Escalation Rules

**Quando fermarsi e richiedere supervisione**:

1. **Impossibilità di installare Node.js 20 LTS**
   - Azione: Escalare a Pipeline Supervisor
   - Blocco: Implementazione bloccata

2. **npm install fallisce ripetutamente per dependency conflict**
   - Azione: Escalare a Pipeline Supervisor con error log
   - Blocco: Package.json non buildabile

3. **Docker non disponibile e richiesto da Execution Blueprint**
   - Azione: Escalare a Pipeline Supervisor
   - Blocco: Dockerfile non testabile localmente (ma resto dell'implementazione procede)

4. **Test fallisce per ragioni non comprese**
   - Azione: Escalare a Reviewer o Architecture per consulenza
   - Blocco: npm test non passa (impossibile completare Definition of Done)

5. **Port binding fallisce anche con PORT env var**
   - Azione: Escalare a Pipeline Supervisor per debug ambiente
   - Blocco: Test manuale server non fattibile

**Criterio di escalation**: Se un'azione richiesta nel workflow è impossibile anche dopo retry ragionevoli (2-3 tentativi), escalare.

---

## Knowledge Candidate Triggers

**Se durante l'implementazione emergono le seguenti situazioni, proporre Knowledge Candidate per consolidamento futuro**:

1. **Nuova prassi Node.js stabile e riutilizzabile**
   - Trigger: Scoprire una pattern Express + Jest + Docker che non è documentata in capability/node.md
   - Proposte: Aggiungere esempio minimalista a capability/node.md

2. **Lezione su Dockerfile minimalista Node.js**
   - Trigger: Il processo di optimizzazione del Dockerfile è notevole
   - Proposte: Creare documento `knowledge-base/patterns/nodejs-docker-minimal.md`

3. **Port configurazione pattern**
   - Trigger: Se il modo di gestire PORT env var e default è inusuale
   - Proposte: Documentare pattern in capability/node.md

---

## Metadata (Addendum)

- **Created**: 2026-06-17 (con Execution Blueprint)
- **Modified**: [data di ultima generazione]
- **Approver**: Pipeline Supervisor (quando Execution Blueprint approved)
- **Status**: Ready for Execution
- **Expected Duration**: 2-4 ore (implementation, testing, docker build)
- **Complexity**: Low (straightforward implementation, no design decisions)

---

**Agent Package Status**: ✅ Complete and ready for Runtime Adapter execution
