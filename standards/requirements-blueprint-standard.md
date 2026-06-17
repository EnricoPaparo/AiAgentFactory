---
standard: requirements-blueprint
applies-to: "projects/*/blueprints/requirements-blueprint.md"
required-sections:
  - "## Source Request"
  - "## Goal"
  - "## Expected Output"
  - "## Functional Requirements"
  - "## Non-Functional Requirements"
  - "## Constraints"
  - "## Assumptions"
  - "## Ambiguities"
  - "## Out Of Scope"
  - "## Acceptance Criteria"
  - "## Initial Risks"
optional-sections:
  - "## Stakeholders"
  - "## Priority Notes"
  - "## Reference Materials"
---

# Requirements Blueprint Standard

## Scopo

Definire il formato minimo del Requirements Blueprint. Questo artefatto chiarisce cosa deve essere costruito, perche, con quali vincoli e con quali criteri di accettazione.

## Creato da

Requirement Analyst.

## Usato da

Architect, Pipeline Designer, Pipeline Supervisor.

## Quando si usa

Si usa all'inizio di un progetto, prima di scegliere architettura, stack o team operativo.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `project-id` | Identificativo del progetto. |
| `source-request` | Richiesta utente originale o sintesi fedele. |
| `goal` | Obiettivo principale. |
| `expected-output` | Output atteso dal progetto. |
| `functional-requirements` | Requisiti funzionali verificabili. |
| `non-functional-requirements` | Requisiti non funzionali noti. |
| `constraints` | Vincoli tecnici, temporali, organizzativi o di piattaforma. |
| `assumptions` | Assunzioni esplicite. |
| `ambiguities` | Ambiguita non risolte o decisioni da chiarire. |
| `out-of-scope` | Cosa non deve essere incluso. |
| `acceptance-criteria` | Criteri di accettazione verificabili. |
| `initial-risks` | Rischi iniziali. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `stakeholders` | Utenti, committenti o reviewer coinvolti. |
| `priority-notes` | Priorita relative tra requisiti. |
| `reference-materials` | Materiali ricevuti o link locali. |

## Formato consigliato

```markdown
# Requirements Blueprint: <project-id>

## Source Request

## Goal

## Expected Output

## Functional Requirements

## Non-Functional Requirements

## Constraints

## Assumptions

## Ambiguities

## Out Of Scope

## Acceptance Criteria

## Initial Risks

## Stakeholders

## Priority Notes

## Reference Materials
```

## Criteri di validita

Un Requirements Blueprint e valido quando:

1. l'obiettivo e comprensibile senza leggere conversazioni esterne;
2. ogni requisito funzionale e verificabile;
3. assunzioni e ambiguita sono separate;
4. i criteri di accettazione possono guidare review finale;
5. non contiene scelte architetturali non richieste;
6. il fuori scope riduce il rischio di espansione implicita del lavoro.

## Failure mode

- Requisiti scritti come desideri generici.
- Assunzioni presentate come fatti.
- Mancano criteri di accettazione.
- Il Requirement Analyst sceglie stack o architettura.
- Ambiguita cancellate invece di essere registrate.

## Esempio minimo

```markdown
# Requirements Blueprint: demo-api

## Source Request

Creare una piccola API demo con endpoint di health check.

## Goal

Fornire una base API minima verificabile.

## Expected Output

Repository con endpoint `GET /health` e test.

## Functional Requirements

- Esporre `GET /health`.
- Restituire HTTP 200.
- Restituire JSON con stato e timestamp.

## Non-Functional Requirements

- Test automatico presente.

## Constraints

- Usare il repository esistente.

## Assumptions

- Il progetto puo usare lo stack gia presente nel repository.

## Ambiguities

- Nessuna autenticazione richiesta.

## Out Of Scope

- Database.
- Deploy.

## Acceptance Criteria

- Il test dell'endpoint passa.
- La risposta contiene `status`.

## Initial Risks

- Stack non ancora identificato.
```
