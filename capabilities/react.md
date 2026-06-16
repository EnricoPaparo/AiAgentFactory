# Capability: react

## Scope

Pratiche operative per modifiche a interfacce React, componenti, stato, routing e integrazione con API.

## Applies When

- Il progetto usa React o framework basati su React.
- Un agente modifica componenti, hook, stato o UI.
- Un Reviewer valuta regressioni frontend.

## Does Not Apply When

- Il task e backend-only.
- La modifica frontend e solo contenuto statico senza logica o layout.

## Operational Practices

- Seguire componenti, naming e design system esistenti.
- Separare stato locale, derivato e remoto.
- Gestire loading, error e empty state quando il flusso li prevede.
- Evitare componenti troppo grandi o duplicazione non necessaria.
- Verificare comportamento responsive quando l'UI cambia layout.

## Checklist

- Il componente segue pattern esistenti?
- Stati loading, error e empty sono gestiti?
- Le props hanno tipi chiari?
- Event handler e side effect sono stabili?
- L'interfaccia resta usabile su viewport rilevanti?

## Failure Modes

- Stato duplicato o derivato manualmente.
- Side effect non controllati in hook.
- Layout che rompe su contenuto lungo.
- UI nuova incoerente con il sistema esistente.

## Review Criteria

- Il comportamento utente soddisfa i criteri di accettazione.
- La UI e coerente con pattern locali.
- Non ci sono regressioni evidenti di accessibilita o responsive behavior.
- Test o verifica manuale sono riportati.

## Risk Signals

- Modifiche a componenti condivisi.
- Form, autenticazione, pagamenti o dati sensibili.
- Rendering condizionale complesso.
- Dipendenze UI nuove.

## Not A Tutorial Boundary

Non spiegare React o hook da zero. Questa capability guida controlli operativi e review.

## Related Capabilities

- testing-strategy
- code-review
- api-security

## Source Knowledge Candidates

None.

## Examples

- Per un componente dati, verificare almeno loading, errore, lista vuota e lista popolata.

## Deprecated Guidance

- Non introdurre pattern di stato globali per stato locale semplice.
