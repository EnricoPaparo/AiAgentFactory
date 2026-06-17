---
standard: solution-blueprint
applies-to: "projects/*/blueprints/solution-blueprint.md"
required-sections:
  - "## Requirements Source"
  - "## Solution Summary"
  - "## Architecture"
  - "## Stack"
  - "## Components"
  - "## Data Flow"
  - "## Integrations"
  - "## Security Considerations"
  - "## Implementation Strategy"
  - "## Trade-Offs"
  - "## Technical Risks"
optional-sections:
  - "## Migration Notes"
  - "## Performance Notes"
  - "## Operational Notes"
---

# Solution Blueprint Standard

## Scopo

Definire il formato minimo del Solution Blueprint. Questo artefatto descrive come soddisfare i requisiti con architettura, stack, componenti, integrazioni, rischi e trade-off.

## Creato da

Architect.

## Usato da

Pipeline Designer, Knowledge Compiler, Pipeline Supervisor.

## Quando si usa

Si usa dopo un Requirements Blueprint valido e prima della progettazione della pipeline operativa.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `project-id` | Identificativo del progetto. |
| `requirements-source` | Percorso del Requirements Blueprint usato. |
| `solution-summary` | Sintesi della soluzione proposta. |
| `architecture` | Architettura logica e componenti principali. |
| `stack` | Tecnologie, linguaggi, librerie o vincoli di stack. |
| `components` | Componenti da creare o modificare. |
| `data-flow` | Flussi dati rilevanti. |
| `integrations` | Sistemi esterni o assenza esplicita di integrazioni. |
| `security-considerations` | Considerazioni minime di sicurezza. |
| `implementation-strategy` | Strategia incrementale di implementazione. |
| `trade-offs` | Decisioni e alternative scartate. |
| `technical-risks` | Rischi tecnici e mitigazioni. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `migration-notes` | Note se il progetto modifica sistemi esistenti. |
| `performance-notes` | Rischi o obiettivi prestazionali. |
| `operational-notes` | Logging, monitoraggio, deploy o manutenzione. |

## Formato consigliato

```markdown
# Solution Blueprint: <project-id>

## Requirements Source

## Solution Summary

## Architecture

## Stack

## Components

## Data Flow

## Integrations

## Security Considerations

## Implementation Strategy

## Trade-Offs

## Technical Risks

## Migration Notes

## Performance Notes

## Operational Notes
```

## Criteri di validita

Un Solution Blueprint e valido quando:

1. soddisfa i criteri di accettazione del Requirements Blueprint;
2. dichiara stack e componenti in modo abbastanza preciso da guidare la pipeline;
3. separa decisioni architetturali da task operativi;
4. registra trade-off e alternative scartate;
5. include rischi tecnici con mitigazioni;
6. non crea agenti o assegna lavoro operativo.

## Failure mode

- Architettura troppo vaga per generare una pipeline.
- Stack scelto senza motivazione.
- Componenti non collegati ai requisiti.
- Rischi tecnici omessi.
- L'Architect anticipa il lavoro del Pipeline Designer.

## Esempio minimo

```markdown
# Solution Blueprint: demo-api

## Requirements Source

projects/demo-api/blueprints/requirements-blueprint.md

## Solution Summary

Implementare un endpoint di health check nel server esistente.

## Architecture

Singolo servizio HTTP con route dedicata.

## Stack

Stack esistente del repository.

## Components

- Route health.
- Test endpoint.

## Data Flow

Client chiama `GET /health`, il server restituisce JSON statico con timestamp.

## Integrations

Nessuna integrazione esterna.

## Security Considerations

Non esporre dati sensibili nella risposta.

## Implementation Strategy

Implementare route, aggiungere test, eseguire test.

## Trade-Offs

Nessun database per mantenere il controllo semplice.

## Technical Risks

- Stack non identificato: mitigare ispezionando il repo prima di implementare.
```
