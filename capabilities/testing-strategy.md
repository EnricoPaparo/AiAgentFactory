# Capability: testing-strategy

## Scope

Scelta, esecuzione e comunicazione dei test essenziali per modifiche software.

## Applies When

- Un agente implementa o modifica comportamento.
- Un Tester verifica criteri di accettazione.
- Un Reviewer valuta evidenza di test.

## Does Not Apply When

- Il task non modifica comportamento verificabile.
- Non esiste ambiente di test e il task richiede solo analisi statica.

## Operational Practices

- Collegare ogni test a un requisito o rischio.
- Preferire test comportamentali rispetto a test dell'implementazione interna.
- Eseguire il set minimo utile per il change set.
- Riportare comandi e risultati nell'handoff.
- Motivare esplicitamente i test non eseguibili.

## Checklist

- Esiste almeno una verifica per il comportamento modificato?
- I casi negativi rilevanti sono coperti?
- I test sono stati eseguiti davvero?
- Il risultato e riportato nell'handoff?
- I test mancanti sono dichiarati come rischio?

## Failure Modes

- Test dichiarati implicitamente ma non eseguiti.
- Test che coprono solo il percorso felice.
- Snapshot o mock che nascondono regressioni reali.
- Nessuna motivazione quando i test non sono disponibili.

## Review Criteria

- I test coprono i criteri di accettazione rilevanti.
- L'evidenza e ripetibile o chiaramente spiegata.
- I fallimenti sono riportati senza essere nascosti.

## Risk Signals

- Modifiche a logica condivisa.
- Bug fix senza test di regressione.
- Refactor con comportamento invariato ma senza verifica.
- Test lenti o fragili usati come unica evidenza.

## Not A Tutorial Boundary

Non spiegare framework di testing. Questa capability definisce come scegliere e comunicare verifiche.

## Related Capabilities

- code-review
- node
- react

## Source Knowledge Candidates

None.

## Examples

- Handoff utile: comando eseguito, risultato, test aggiunti, limiti della copertura.

## Deprecated Guidance

- Non considerare "nessun errore visibile" come test.
