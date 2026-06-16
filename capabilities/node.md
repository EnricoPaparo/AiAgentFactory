# Capability: node

## Scope

Pratiche operative per progetti Node.js o TypeScript lato server, script, CLI o tooling.

## Applies When

- Il repository usa Node.js, npm, pnpm, yarn o TypeScript.
- Un agente deve modificare API, script, servizi o tooling Node.
- Un Reviewer deve valutare modifiche in un progetto Node.

## Does Not Apply When

- Il progetto non usa runtime Node.
- La modifica e puramente documentale.

## Operational Practices

- Rispettare package manager e script gia presenti.
- Controllare `package.json` prima di aggiungere dipendenze.
- Preferire API e pattern esistenti nel repo.
- Gestire errori asincroni in modo esplicito.
- Evitare nuove dipendenze senza motivazione.

## Checklist

- Il package manager usato e quello del repo?
- Gli script necessari sono documentati o eseguiti?
- Le modifiche TypeScript rispettano tipi e build?
- Errori e promise rejection sono gestiti?
- Nuove dipendenze sono necessarie e motivate?

## Failure Modes

- Mescolare package manager.
- Aggiungere dipendenze per problemi risolvibili con codice esistente.
- Ignorare error handling asincrono.
- Cambiare configurazioni globali per sistemare un caso locale.

## Review Criteria

- La modifica segue i pattern Node gia presenti.
- Build o test pertinenti sono stati eseguiti.
- Le dipendenze sono giustificate.
- Input, errori e side effect sono gestiti.

## Risk Signals

- Modifiche a script di build o deploy.
- Aggiornamenti di dipendenze transitive.
- Uso di variabili ambiente o filesystem.
- Codice asincrono senza gestione errori.

## Not A Tutorial Boundary

Non spiegare Node.js, npm o TypeScript da zero. Questa capability guida decisioni operative in repo Node.

## Related Capabilities

- testing-strategy
- api-security
- git-workflow

## Source Knowledge Candidates

None.

## Examples

- Prima di aggiungere una libreria, verificare se esiste gia una utility locale equivalente.

## Deprecated Guidance

- Non introdurre un secondo package manager nello stesso progetto.
