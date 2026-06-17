# Human Gates

Contiene le validazioni umane bloccanti del progetto.

## Standard

- `standards/human-gate-standard.md`

## Regole

- Un gate con stato `Pending` blocca i task downstream inclusi nel suo `blocking-scope`.
- Il processo riprende solo con gate `Approved`, oppure torna alla fase indicata se `Changes Requested`.
- Le decisioni devono includere autore, data e note.
