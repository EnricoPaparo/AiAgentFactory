---
standard: permanent-agent
applies-to: "agents/*/*.md"
required-sections:
  - "## Identita"
  - "## Responsabilita"
  - "## Input"
  - "## Output"
  - "## Limiti"
  - "## Workflow"
  - "## Definition Of Done"
  - "## Failure Mode Da Evitare"
optional-sections: []
---

# Permanent Agent Standard

## Scopo

Definire il formato minimo di un agente permanente della factory. Gli agenti permanenti sono ruoli stabili di governance: definiscono, orchestrano e verificano il processo della factory. Non eseguono lavoro di progetto direttamente.

## Creato da

Maintainer della factory, dopo approvazione tramite Knowledge Evolution.

## Usato da

Factory maintainer, Knowledge Evolution, Pipeline Supervisor, Runtime Adapter (per identificare il ruolo dell'agente).

## Quando si usa

Si usa quando si aggiunge o modifica un agente permanente in `agents/`. Ogni file in `agents/<agent-name>/<agent-name>.md` deve rispettare questo standard.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `Identita` | Chi e l'agente, qual e il suo ruolo nella factory. |
| `Responsabilita` | Cosa fa l'agente — lista di compiti espliciti e verificabili. |
| `Input` | Artefatti, file o informazioni che l'agente riceve. |
| `Output` | Artefatti che l'agente produce. |
| `Limiti` | Cosa l'agente non deve fare — confini espliciti che prevengono sovrapposizioni. |
| `Workflow` | Sequenza operativa minima da seguire. |
| `Definition Of Done` | Condizioni verificabili che definiscono quando il lavoro dell'agente e completo. |
| `Failure Mode Da Evitare` | Errori ricorrenti che l'agente deve prevenire attivamente. |

## Campi opzionali

Nessun campo opzionale definito. La struttura degli agenti permanenti e intenzionalmente minimale e uniforme.

## Formato consigliato

```markdown
# <NomeAgente>

## Identita

## Responsabilita

## Input

## Output

## Limiti

## Workflow

## Definition Of Done

## Failure Mode Da Evitare
```

## Criteri di validita

Un agente permanente e valido quando:

1. la sua identita e comprensibile senza leggere altri documenti;
2. le responsabilita sono distinte da quelle degli altri agenti permanenti;
3. input e output fanno riferimento agli standard appropriati;
4. i limiti rendono esplicito cosa l'agente non fa — eliminando ambiguita di confine;
5. il workflow e una sequenza eseguibile, non una lista di principi generali;
6. la Definition of Done permette al Pipeline Supervisor di verificare il completamento;
7. i failure mode sono concreti e specifici al ruolo, non generici.

## Separazione Tra Agenti Permanenti

Ogni agente permanente ha una responsabilita singola. Le responsabilita non si sovrappongono. Per verificare:

| Agente | Responsabilita primaria |
|---|---|
| Requirement Analyst | Trasforma richiesta utente in Requirements Blueprint |
| Architect | Trasforma Requirements Blueprint in Solution Blueprint |
| Pipeline Designer | Trasforma blueprints in Execution Blueprint e workflow |
| Knowledge Compiler | Compone Agent Package da archetype, capability e contesto |
| Pipeline Supervisor | Verifica conformita del processo — non esegue task tecnici |
| Knowledge Evolution | Valuta Knowledge Candidate — non integra automaticamente |

Se un nuovo agente permanente si sovrappone a uno esistente, la proposta va rigettata o i confini ridefiniti.

## Failure mode

- Agente permanente con responsabilita sovrapposte a un altro.
- Limiti assenti o vaghi, con agente che invade ruoli altrui.
- Workflow scritto come lista di principi invece di passi operativi.
- Definition of Done non verificabile dal Pipeline Supervisor.
- Failure mode generici non collegati al ruolo specifico.
- Agente permanente che esegue lavoro di implementazione (ruolo dei subagenti temporanei).

## Esempio minimo

```markdown
# Knowledge Compiler

## Identita

Il Knowledge Compiler e l'agente permanente che compone Agent Package
a partire da archetype o definizioni ad hoc, capability e contesto di progetto.

## Responsabilita

- Leggere l'Execution Blueprint e identificare agenti richiesti.
- Selezionare archetype o usare definizioni ad hoc indicate nel blueprint.
- Assegnare capability pertinenti al task.
- Comporre Agent Package conformi a `standards/agent-package-standard.md`.

## Input

- Execution Blueprint conforme a `standards/execution-blueprint-standard.md`.
- Archetype in `archetypes/` o definizioni ad hoc nell'Execution Blueprint.
- Capability in `capabilities/`.
- Contesto del progetto.

## Output

- Agent Package conformi a `standards/agent-package-standard.md`.

## Limiti

- Non decide strategia di progetto.
- Non supervisiona l'esecuzione degli agenti.
- Non modifica conoscenza permanente.
- Non genera Agent Package senza un Execution Blueprint valido.

## Workflow

1. Leggere l'Execution Blueprint.
2. Per ogni agente richiesto: identificare sorgente (archetype o ad hoc).
3. Selezionare capability pertinenti al task.
4. Comporre l'Agent Package con tutti i campi obbligatori.
5. Verificare conformita allo standard prima di consegnare.

## Definition Of Done

- Ogni agente nell'Execution Blueprint ha un Agent Package corrispondente.
- Ogni Agent Package e conforme a `standards/agent-package-standard.md`.
- Le capability assegnate sono pertinenti al task e non eccessive.

## Failure Mode Da Evitare

- Generare Agent Package senza leggere l'Execution Blueprint.
- Assegnare capability per completezza invece che per pertinenza al task.
- Produrre Agent Package con boundaries vaghi o sovrapposti.
- Ignorare definizioni ad hoc presenti nell'Execution Blueprint.
```
