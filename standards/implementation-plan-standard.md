---
standard: implementation-plan
applies-to: "projects/*/blueprints/implementation-plan.md"
required-sections:
  - "## Metadata"
  - "## Scope Summary"
  - "## Module Breakdown"
  - "## Dependency Graph"
  - "## Chunking Strategy"
  - "## Parallelism Opportunities"
  - "## Risk Notes"
optional-sections:
  - "## Estimated Effort"
  - "## Tech Notes"
  - "## Open Questions"
---

# Implementation Plan Standard

## Scopo

Definire il formato dell'Implementation Plan: l'artefatto che decompone
un Solution Blueprint in moduli concreti, dimensionati e ordinati, pronti
per essere trasformati in step di pipeline dal Pipeline Designer.

Senza questo artefatto, il Pipeline Designer non sa quanto è grande ogni
componente, quali dipendono da altri, e dove chunkare. Con questo artefatto,
la decomposizione in step non è una stima cieca ma una scelta informata.

## Creato da

Implementation Planner.

## Usato da

Pipeline Designer (per creare workflow.yml con step correttamente dimensionati).

## Campi obbligatori

### ## Metadata

| Campo | Descrizione |
|---|---|
| `project-id` | Identificativo del progetto. |
| `based-on` | File del Solution Blueprint di riferimento. |
| `created-by` | `implementation-planner` |
| `version` | Versione del piano. |

### ## Scope Summary

Riepilogo in 3-5 righe di cosa viene costruito, perché, e qual è il confine
del lavoro coperto da questo piano.

### ## Module Breakdown

Tabella di tutti i moduli/componenti da implementare. Per ogni modulo:

| Campo | Descrizione |
|---|---|
| `module-id` | Identificatore kebab-case unico. |
| `description` | Cosa fa questo modulo. |
| `size` | `small` (< 200 righe), `medium` (200-600), `large` (> 600). |
| `complexity` | `low`, `medium`, `high`. |
| `dependencies` | Lista di module-id che devono essere completati prima. |
| `can-parallelize` | `yes` / `no` — può girare in parallelo con altri senza dipendenze condivise. |
| `agent-type` | Tipo di agente temporaneo consigliato (es. `developer`, `specialist`). |

### ## Dependency Graph

Rappresentazione testuale o ASCII del grafo delle dipendenze tra moduli.
Deve essere leggibile da un agente per costruire l'ordine corretto degli step.

Esempio:
```
auth-module ──→ user-api ──→ integration-tests
db-schema   ──↗
```

### ## Chunking Strategy

Descrizione esplicita di come raggruppare i moduli in step di pipeline.
Ogni chunk deve stare comodamente entro i limiti di output di un singolo agente
(indicativamente: max 2-3 moduli `small`, 1 modulo `medium`, oppure una
parte ben delimitata di un modulo `large`).

Per ogni chunk proposto:
- Quali moduli include.
- Perché questi moduli stanno insieme (coesione logica).
- Step ID suggerito per il workflow.yml.

### ## Parallelism Opportunities

Lista di gruppi di chunk che possono essere eseguiti in parallelo perché
non condividono dipendenze. Il Pipeline Designer usa questa lista per
costruire i blocchi `parallel:` nel workflow.yml.

### ## Risk Notes

Moduli o dipendenze che rappresentano rischi per l'esecuzione:
- Moduli `large` + `high` complexity che potrebbero richiedere più step.
- Dipendenze esterne non ancora confermate.
- Aree dove le assunzioni del Solution Blueprint sono più fragili.

## Sezioni opzionali

### ## Estimated Effort

Stima del numero totale di step di pipeline e API call previste.
Utile per stimare il costo prima di lanciare.

### ## Tech Notes

Note tecniche specifiche per l'implementazione (convenzioni di naming,
pattern da seguire, struttura di directory attesa).

### ## Open Questions

Domande non risolte che il Pipeline Designer o gli agenti esecutivi
potrebbero dover risolvere durante l'implementazione.
