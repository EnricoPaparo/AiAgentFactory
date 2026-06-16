# Capability: code-review

## Scope

Review tecnica di modifiche software, con priorita a bug, regressioni, rischi, test mancanti e coerenza con blueprint e Agent Package.

## Applies When

- Un Reviewer valuta codice o configurazione.
- Un Developer vuole auto-controllare un diff prima dell'handoff.
- Un Pipeline Supervisor deve verificare che una review sia sostanziale.

## Does Not Apply When

- Il task e solo documentale e non impatta comportamento tecnico.
- Serve un audit specialistico coperto da capability piu specifica.

## Operational Practices

- Leggere prima requisiti, soluzione, task e handoff.
- Valutare comportamento, non solo stile.
- Ordinare i problemi per severita.
- Collegare ogni finding a file, area o criterio verificabile.
- Dichiarare test mancanti o non eseguiti.

## Checklist

- Il diff soddisfa il task assegnato?
- Esistono regressioni plausibili?
- Gli error path sono gestiti?
- I test coprono il comportamento modificato?
- L'handoff dichiara rischi residui?

## Failure Modes

- Review estetica senza rischi reali.
- Approvazione basata solo su lettura superficiale.
- Finding non riproducibili o non azionabili.
- Mancata verifica dei test.

## Review Criteria

- I finding sono concreti, ordinati e verificabili.
- La review distingue blocchi da suggerimenti.
- L'esito finale e esplicito: approve, request changes o blocked.

## Risk Signals

- Modifica a codice condiviso senza test.
- Cambiamenti di sicurezza, autenticazione o dati.
- Handoff incompleto.
- Diff troppo grande rispetto al task.

## Not A Tutorial Boundary

Non spiegare principi generici di code review. Usare questa capability per guidare controlli operativi.

## Related Capabilities

- testing-strategy
- api-security
- git-workflow

## Source Knowledge Candidates

None.

## Examples

- Finding valido: "Il nuovo endpoint accetta input non validato e non ha test per payload vuoto."

## Deprecated Guidance

- Non usare "LGTM" come unico output di review.
