# Capability: documentation

## Scope

Pratiche operative per creare o aggiornare documentazione tecnica, operativa o di progetto in modo verificabile.

## Applies When

- Un Documentation Writer produce o aggiorna documenti.
- Un Developer modifica comportamento che richiede documentazione.
- Un Reviewer valuta accuratezza documentale.

## Does Not Apply When

- Il task non produce conoscenza da conservare.
- La documentazione richiesta e specialistica e coperta da capability piu specifica.

## Operational Practices

- Documentare il comportamento reale, non intenzioni future.
- Collegare istruzioni a file, comandi o artefatti esistenti.
- Esplicitare limiti, assunzioni e stato.
- Aggiornare la fonte corretta invece di duplicare informazioni.
- Tenere separata documentazione di progetto e conoscenza permanente.

## Checklist

- La documentazione corrisponde al deliverable reale?
- I riferimenti a file e comandi sono corretti?
- Le assunzioni sono dichiarate?
- Eventuali limiti o problemi aperti sono visibili?
- Il contenuto appartiene alla destinazione scelta?

## Failure Modes

- Documentare funzionalita non implementate.
- Copiare testo generico non collegato al progetto.
- Nascondere workaround o problemi aperti.
- Inserire conoscenza locale tra gli standard permanenti.

## Review Criteria

- Il lettore puo usare il documento senza contesto esterno essenziale.
- Le affermazioni sono verificabili.
- Non ci sono contraddizioni con blueprint, handoff o codice.
- La collocazione del documento e corretta.

## Risk Signals

- Documentazione di installazione o deploy.
- Istruzioni che includono segreti o credenziali.
- Divergenza tra README e comportamento reale.
- Nuove regole permanenti proposte senza Knowledge Candidate.

## Not A Tutorial Boundary

Non trasformare ogni documento in guida didattica. Questa capability mantiene la documentazione precisa e operativa.

## Related Capabilities

- git-workflow
- code-review

## Source Knowledge Candidates

None.

## Examples

- Un handoff documentale deve indicare fonti usate, file aggiornati e assunzioni editoriali.

## Deprecated Guidance

- Non duplicare informazioni gia presenti se e possibile aggiornare la fonte autorevole.
