---
standard: handoff
applies-to: "projects/[!_]*/handoffs/*.md"
required-sections:
  - "## Metadata"
  - "## Completed Task Or Phase"
  - "## Produced Output"
  - "## Involved Files"
  - "## Decisions Made"
  - "## Open Issues"
  - "## Residual Risks"
  - "## Requested Next Action"
  - "## Verification Criteria"
optional-sections:
  - "## Blocked Items"
  - "## Knowledge Candidates"
  - "## Test Evidence"
  - "## Review Notes"
---

# Handoff Standard

## Scopo

Definire il formato minimo di un handoff tra agenti, fasi o responsabilita. Un handoff rende verificabile cosa e stato prodotto, cosa resta aperto e quale azione deve seguire.

## Creato da

Agente o fase mittente.

## Usato da

Agente o fase destinataria, Pipeline Supervisor, Knowledge Evolution quando emergono lezioni riutilizzabili.

## Quando si usa

Si usa ogni volta che un output passa da una responsabilita a un'altra: tra agenti permanenti, tra subagenti temporanei, tra esecuzione e review, o alla chiusura del progetto.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `handoff-id` | Identificativo in kebab-case, unico nel progetto. |
| `project-id` | Identificativo del progetto workspace. |
| `sender` | Agente o fase che consegna. |
| `recipient` | Agente o fase che riceve. |
| `completed-task-or-phase` | Task o fase completata. |
| `produced-output` | Output consegnato. |
| `involved-files` | File o artefatti coinvolti. |
| `decisions-made` | Decisioni prese durante il lavoro. |
| `open-issues` | Problemi aperti. Usare `None` se assenti. |
| `residual-risks` | Rischi residui. Usare `None` se assenti. |
| `requested-next-action` | Azione richiesta al destinatario. |
| `verification-criteria` | Come verificare l'output. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `blocked-items` | Elementi bloccati e motivo. |
| `knowledge-candidates` | Proposte emerse durante il lavoro. |
| `test-evidence` | Comandi, controlli o prove eseguite. |
| `review-notes` | Note utili per il reviewer o supervisor. |

## Formato consigliato

```markdown
# Handoff: <handoff-id>

## Metadata

- handoff-id:
- project-id:
- sender:
- recipient:

## Completed Task Or Phase

## Produced Output

## Involved Files

## Decisions Made

## Open Issues

## Residual Risks

## Requested Next Action

## Verification Criteria

## Blocked Items

## Knowledge Candidates

## Test Evidence

## Review Notes
```

## Criteri di validita

Un handoff e valido quando:

1. mittente e destinatario sono espliciti;
2. output e file coinvolti sono identificabili;
3. la prossima azione e assegnabile;
4. problemi aperti e rischi residui non sono omessi;
5. i criteri di verifica permettono al destinatario o al Pipeline Supervisor di controllare l'output;
6. non contiene nuove decisioni strategiche non tracciate nei blueprint.

## Failure mode

- Handoff narrativo, ma non verificabile.
- Mancano file coinvolti o output reali.
- Problemi aperti nascosti o descritti in modo generico.
- Prossima azione non assegnata.
- Verifica demandata al giudizio soggettivo.

## Esempio minimo

```markdown
# Handoff: developer-to-reviewer-health-endpoint

## Metadata

- handoff-id: developer-to-reviewer-health-endpoint
- project-id: demo-api
- sender: Developer
- recipient: Reviewer

## Completed Task Or Phase

Implementazione endpoint `GET /health`.

## Produced Output

- Endpoint funzionante.
- Test automatico dedicato.

## Involved Files

- src/routes/health.ts
- tests/health.test.ts

## Decisions Made

- Risposta JSON con `status` e `timestamp`.

## Open Issues

None.

## Residual Risks

None.

## Requested Next Action

Eseguire review tecnica e verificare i test.

## Verification Criteria

- Test suite verde.
- Endpoint restituisce HTTP 200.
```
