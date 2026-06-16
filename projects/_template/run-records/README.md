# Run Records

Contiene record auditabili delle azioni operative della factory.

## Standard

- `standards/run-record-standard.md`

## Regole

- Ogni approval gestita dal runner crea un run record.
- Ogni esecuzione agente dovrebbe dichiarare runtime packet, input usati, output e verifiche.
- Pipeline Supervisor puo usare questi record per verificare il processo senza ricostruire tutta la conversazione.
