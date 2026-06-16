# Runtime Packets

Contiene contesti compatti per eseguire Agent Package senza rileggere tutta la factory.

## Standard

- `standards/runtime-packet-standard.md`

## Regole

- Ogni agente temporaneo dovrebbe avere un runtime packet.
- Il packet contiene solo contesto approvato e file strettamente necessari.
- Se cambia un blueprint approvato, i packet downstream devono essere rigenerati.
