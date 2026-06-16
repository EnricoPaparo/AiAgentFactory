# Pilot: Agent Package Validation

Questo progetto pilota valida la factory su un task documentale piccolo: produrre una checklist operativa per verificare se un Agent Package e pronto per essere eseguito con il Manual Execution Adapter.

## Obiettivo Del Pilota

Verificare il ciclo:

```text
initial request
-> requirements blueprint
-> solution blueprint
-> execution blueprint
-> generated agent package
-> manual execution
-> deliverable
-> handoff
-> review
-> closure
```

## Primo Agente Da Eseguire

Eseguire:

```text
projects/pilot-agent-package-validation/generated-agents/documentation-writer-agent-package.md
```

usando:

```text
runtime-adapters/manual-execution.md
```

## Output Atteso Dal Primo Run

- `projects/pilot-agent-package-validation/deliverables/agent-package-validation-checklist.md`
- `projects/pilot-agent-package-validation/handoffs/documentation-writer-to-reviewer.md`

## Nota Su Human Gate

Il gate finale `approve-final-delivery.md` e `Pending`, ma blocca solo `project closure`. Non blocca l'esecuzione del Documentation Writer.
