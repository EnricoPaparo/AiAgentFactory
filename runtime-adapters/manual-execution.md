# Runtime Adapter: Manual Execution

## Scopo

Tradurre un Agent Package generico in una procedura eseguibile manualmente da una persona o da un assistente operativo, senza introdurre un orchestratore automatico.

## Quando Usarlo

Usare questo adapter per:

- prima esecuzione pilota della factory;
- task piccoli o medi dove l'automazione non e ancora necessaria;
- validare standard, handoff, human gate e Knowledge Candidate;
- eseguire agenti temporanei in modo controllato prima di creare adapter runtime-specifici.

## Input Richiesti

- Agent Package conforme a `standards/agent-package-standard.md`.
- Execution Blueprint conforme a `standards/execution-blueprint-standard.md`.
- Human Gate rilevanti, se presenti, conformi a `standards/human-gate-standard.md`.
- Capability assegnate.
- Archetype o definizione ad hoc indicata dall'Agent Package.
- Project Workspace del progetto.

## Output Richiesti

- Deliverable indicati dall'Agent Package.
- Handoff conforme a `standards/handoff-standard.md`.
- Review evidence, se richiesta dal workflow.
- Knowledge Candidate conforme a `standards/knowledge-candidate-standard.md`, se emergono miglioramenti riutilizzabili.
- Stato finale dichiarato: completed, blocked, changes-requested o failed.

## Regola Principale

Il Manual Execution Adapter non decide strategia, scope o architettura. Traduce e applica istruzioni gia presenti in Agent Package, blueprint, standard e gate.

## Procedura Di Esecuzione

### 1. Preflight

Prima di eseguire il task:

1. leggere Agent Package completo;
2. verificare che `project-id`, `agent-role`, `agent-source`, `assigned-capabilities`, `task`, `expected-outputs`, `boundaries`, `workflow` e `definition-of-done` siano presenti;
3. leggere Execution Blueprint;
4. leggere capability assegnate;
5. leggere archetype o definizione ad hoc indicata da `agent-source`;
6. controllare se esistono Human Gate nel Project Workspace;
7. controllare eventuali handoff richiesti come input.

Se manca un input obbligatorio, fermarsi e produrre stato `blocked`.

### 2. Human Gate Check

Prima di qualunque task operativo:

1. cercare Human Gate con stato `Pending`;
2. confrontare `blocking-scope` con il task corrente;
3. se il task rientra nel blocking scope, fermarsi;
4. chiedere validazione umana;
5. riprendere solo quando il gate e `Approved`.

Comportamento per stato:

| Stato | Comportamento |
|---|---|
| `Pending` | Fermarsi e attendere decisione umana. |
| `Approved` | Proseguire. |
| `Changes Requested` | Tornare alla fase indicata in `return-to-phase`. |
| `Rejected` | Bloccare o chiudere secondo Execution Blueprint. |
| `Cancelled` | Ignorare il gate se non esiste altro blocco. |
| `Expired` | Fermarsi e chiedere nuova decisione o escalation. |

### 3. Esecuzione Del Task

Eseguire il workflow dell'Agent Package nell'ordine indicato.

Regole operative:

- rispettare sempre i `boundaries`;
- non aggiungere output non richiesti;
- non modificare conoscenza permanente;
- non cambiare blueprint o standard durante l'esecuzione del task;
- registrare decisioni operative rilevanti;
- registrare problemi aperti appena emergono;
- se emerge una lezione riutilizzabile, creare o proporre una Knowledge Candidate.

### 4. Verifica Locale

Prima dell'handoff:

1. controllare ogni elemento della Definition of Done;
2. eseguire test, review o controlli richiesti dalle capability;
3. se una verifica non e eseguibile, registrare motivo e rischio residuo;
4. non dichiarare completato un task con verifiche obbligatorie mancanti.

### 5. Produzione Handoff

Ogni esecuzione deve produrre un handoff conforme a `standards/handoff-standard.md`.

L'handoff deve includere almeno:

- agente o fase mittente;
- destinatario;
- task completato o bloccato;
- output prodotto;
- file o artefatti coinvolti;
- decisioni prese;
- problemi aperti;
- rischi residui;
- prossima azione richiesta;
- criteri per verificare l'output;
- test evidence, se pertinente.

### 6. Review Evidence

Se l'Execution Blueprint richiede review gate:

- indicare quale gate deve essere eseguito;
- indicare quale agente o ruolo deve revisionare;
- fornire artefatti e handoff necessari;
- non segnare il gate come superato senza review esplicita.

### 7. Knowledge Candidate

Creare una Knowledge Candidate quando:

- una pratica emersa sembra riutilizzabile;
- un agente ad hoc potrebbe diventare archetype;
- una capability e insufficiente o troppo generica;
- uno standard genera ambiguita;
- un failure mode ricorrente viene scoperto;
- un runtime adapter necessita di una nuova regola.

Non integrare direttamente la Knowledge Candidate nella conoscenza permanente.

## Stati Finali

| Stato | Significato |
|---|---|
| `completed` | Task completato, handoff prodotto, DoD soddisfatta. |
| `blocked` | Task fermo per input mancante, Human Gate, errore o decisione richiesta. |
| `changes-requested` | Una review o Human Gate richiede modifiche. |
| `failed` | Task non completabile nel contesto disponibile. |

## Template Di Esecuzione Manuale

```markdown
# Manual Execution Run: <package-id>

## Metadata

- project-id:
- package-id:
- agent-role:
- agent-source:
- executor:
- started-at:
- completed-at:
- final-status:

## Inputs Checked

## Human Gate Check

## Execution Notes

## Verification Evidence

## Produced Outputs

## Handoff Created

## Review Gates Triggered

## Knowledge Candidates Created

## Blockers Or Residual Risks
```

## Esempio Minimo

```markdown
# Manual Execution Run: developer-node-api

## Metadata

- project-id: demo-api
- package-id: developer-node-api
- agent-role: Developer
- agent-source: archetype `archetypes/developer.md`
- executor: Manual Operator
- started-at:
- completed-at:
- final-status: completed

## Inputs Checked

- Agent Package present.
- Execution Blueprint present.
- Capability `capabilities/node.md` present.
- Capability `capabilities/testing-strategy.md` present.

## Human Gate Check

No Pending Human Gate blocking this task.

## Execution Notes

Implemented endpoint `GET /health`.

## Verification Evidence

Test command executed and passed.

## Produced Outputs

- Endpoint implementation.
- Test file.

## Handoff Created

projects/demo-api/handoffs/developer-to-reviewer-health-endpoint.md

## Review Gates Triggered

- Code review.
- Test evidence review.

## Knowledge Candidates Created

None.

## Blockers Or Residual Risks

None.
```

## Failure Mode Da Evitare

- Eseguire task downstream con Human Gate `Pending`.
- Saltare la lettura delle capability assegnate.
- Produrre output senza handoff.
- Dichiarare completato un task senza verificare la Definition of Done.
- Integrare Knowledge Candidate senza Knowledge Evolution.
- Usare questo adapter per prendere decisioni architetturali nuove.

## Criteri Di Completamento Dell'Adapter

Questo adapter e applicato correttamente quando:

1. l'Agent Package e stato letto e verificato;
2. i Human Gate sono stati controllati;
3. il task e stato eseguito nel rispetto dei boundaries;
4. la Definition of Done e stata verificata;
5. e stato prodotto un handoff;
6. review gate e Knowledge Candidate sono stati gestiti secondo standard;
7. lo stato finale e esplicito.
