---
standard: capability
applies-to: "capabilities/*.md"
required-sections:
  - "## Scope"
  - "## Applies When"
  - "## Does Not Apply When"
  - "## Operational Practices"
  - "## Checklist"
  - "## Failure Modes"
  - "## Review Criteria"
  - "## Risk Signals"
  - "## Not A Tutorial Boundary"
optional-sections:
  - "## Related Capabilities"
  - "## Source Knowledge Candidates"
  - "## Examples"
  - "## Deprecated Guidance"
---

# Capability Standard

## Scopo

Definire il formato minimo di una capability. Una capability contiene conoscenza tecnica operativa riutilizzabile, non tutorial generici.

## Creato da

Knowledge Evolution o maintainer della factory, dopo approvazione di conoscenza riutilizzabile.

## Usato da

Knowledge Compiler, subagenti temporanei, Reviewer, Pipeline Supervisor.

## Quando si usa

Si usa per codificare pratiche operative, checklist, failure mode, rischi e criteri di review legati a una tecnologia, dominio o pratica.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `capability-id` | Identificativo in kebab-case. |
| `scope` | Ambito coperto dalla capability. |
| `applies-when` | Quando assegnarla a un agente. |
| `does-not-apply-when` | Quando non assegnarla. |
| `operational-practices` | Pratiche operative essenziali. |
| `checklist` | Controlli da eseguire. |
| `failure-modes` | Errori ricorrenti da prevenire. |
| `review-criteria` | Criteri per valutare output collegati alla capability. |
| `risk-signals` | Segnali che richiedono attenzione o escalation. |
| `not-a-tutorial-boundary` | Cosa non deve contenere. |

## Campi opzionali

| Campo | Descrizione |
|---|---|
| `related-capabilities` | Capability collegate. |
| `source-knowledge-candidates` | Proposte da cui deriva. |
| `examples` | Esempi brevi, solo se operativi. |
| `deprecated-guidance` | Pratiche non piu consigliate. |

## Formato consigliato

```markdown
# Capability: <capability-id>

## Scope

## Applies When

## Does Not Apply When

## Operational Practices

## Checklist

## Failure Modes

## Review Criteria

## Risk Signals

## Not A Tutorial Boundary

## Related Capabilities

## Source Knowledge Candidates

## Examples

## Deprecated Guidance
```

## Criteri di validita

Una capability e valida quando:

1. ha un ambito chiaro;
2. aiuta un agente a lavorare meglio in un task reale;
3. contiene checklist e failure mode verificabili;
4. non spiega concetti base come un corso;
5. non duplica responsabilita dell'archetype;
6. puo essere assegnata dal Knowledge Compiler senza riscriverla.

## Failure mode

- Capability troppo ampia, per esempio `backend.md`.
- Testo didattico invece di pratica operativa.
- Checklist non verificabile.
- Contiene policy di processo che dovrebbero stare in `standards/`.
- Contiene decisioni valide solo per un progetto.

## Esempio minimo

```markdown
# Capability: testing-strategy

## Scope

Scelta e verifica dei test essenziali per task software piccoli o medi.

## Applies When

- Un agente deve modificare codice.
- Un reviewer deve valutare evidenza di test.

## Does Not Apply When

- Il task e solo documentale.

## Operational Practices

- Collegare ogni test a un comportamento richiesto.
- Riportare comandi eseguiti e risultato.

## Checklist

- Esiste almeno un test per il comportamento modificato?
- Il risultato dei test e riportato nell'handoff?

## Failure Modes

- Test non eseguiti ma dichiarati implicitamente.
- Test che verificano implementazione invece di comportamento.

## Review Criteria

- I test coprono i criteri di accettazione rilevanti.

## Risk Signals

- Modifiche condivise senza test.

## Not A Tutorial Boundary

Non spiegare come funziona un framework di testing.
```
