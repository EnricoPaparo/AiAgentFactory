# Capability: git-workflow

## Scope

Uso operativo di Git in un progetto software gestito dalla factory: lettura dello stato, isolamento delle modifiche, commit reviewable e protezione del lavoro esistente.

## Applies When

- Un agente deve modificare file in un repository Git.
- Un Reviewer deve controllare scope e pulizia di un change set.
- Un Pipeline Supervisor deve verificare che le modifiche siano tracciabili.

## Does Not Apply When

- Il task non usa un repository Git.
- L'agente lavora solo su artefatti temporanei fuori controllo versione.

## Operational Practices

- Controllare sempre lo stato del working tree prima di modificare.
- Distinguere modifiche proprie da modifiche preesistenti.
- Tenere il change set coerente con il task assegnato.
- Non revertire modifiche non proprie senza richiesta esplicita.
- Usare messaggi di commit descrittivi quando il workflow richiede commit.

## Checklist

- `git status` e stato controllato prima delle modifiche?
- I file modificati sono collegati al task?
- Sono presenti modifiche preesistenti da preservare?
- Il diff e reviewable?
- Il commit, se richiesto, descrive cosa cambia e perche?

## Failure Modes

- Revert involontario di lavoro altrui.
- Commit con scope misto.
- File generati o temporanei inclusi senza motivo.
- Modifiche non tracciate lasciate fuori dall'handoff.

## Review Criteria

- Il diff e coerente con l'Agent Package.
- Non ci sono modifiche estranee al task.
- Le modifiche preesistenti sono state rispettate.
- Lo stato Git finale e dichiarato nell'handoff.

## Risk Signals

- Working tree sporco prima dell'intervento.
- Modifiche in file condivisi o di configurazione globale.
- Necessita di comandi distruttivi.
- Divergenza tra branch locale e remoto.

## Not A Tutorial Boundary

Non spiegare comandi Git di base. Questa capability definisce pratiche operative e rischi.

## Related Capabilities

- code-review
- testing-strategy

## Source Knowledge Candidates

None.

## Examples

- Prima di editare: registrare se `git status --short` mostra modifiche preesistenti.
- In handoff: indicare file modificati e test eseguiti.

## Deprecated Guidance

- Non usare reset distruttivi come scorciatoia di pulizia.
