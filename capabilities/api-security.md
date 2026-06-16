# Capability: api-security

## Scope

Controlli operativi di sicurezza per API HTTP, input, autenticazione, autorizzazione, dati sensibili ed error handling.

## Applies When

- Un agente crea o modifica endpoint API.
- Una soluzione espone dati o operazioni via rete.
- Un Reviewer o Security Auditor valuta rischi applicativi.

## Does Not Apply When

- Il task non espone superfici API.
- La modifica e solo documentale e non descrive comportamento API.

## Operational Practices

- Validare input al confine dell'API.
- Non esporre segreti, stack trace o dati sensibili.
- Verificare autenticazione e autorizzazione dove richieste.
- Usare codici di errore coerenti e non ambigui.
- Considerare rate, abuso e accesso non previsto quando rilevante.

## Checklist

- Gli input esterni sono validati?
- Le risposte escludono dati sensibili?
- Autenticazione e autorizzazione sono coerenti con i requisiti?
- Gli errori sono gestiti senza leak informativi?
- I test coprono almeno un caso negativo rilevante?

## Failure Modes

- Fidarsi di input client-side.
- Restituire dettagli interni negli errori.
- Confondere autenticazione con autorizzazione.
- Aggiungere endpoint non documentati o fuori scope.

## Review Criteria

- I confini dell'API sono chiari.
- I rischi principali sono mitigati o dichiarati.
- Le risposte e gli errori sono coerenti.
- I test o la review coprono casi di input non valido.

## Risk Signals

- Endpoint pubblici.
- Dati personali o token.
- Operazioni distruttive.
- Upload file o input complessi.
- Bypass temporanei di autorizzazione.

## Not A Tutorial Boundary

Non spiegare sicurezza web generale. Questa capability definisce controlli applicabili al task.

## Related Capabilities

- node
- code-review
- testing-strategy

## Source Knowledge Candidates

None.

## Examples

- Per un endpoint pubblico, verificare input non valido, errore prevedibile e assenza di stack trace.

## Deprecated Guidance

- Non accettare "verra protetto dopo" come mitigazione senza rischio tracciato.
