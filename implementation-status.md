# Implementation Status

Questo documento traccia lo stato di implementazione della factory rispetto alla struttura e agli MVP definiti in `AgentFactory.md`.

## Baseline

- Data verifica: 2026-06-16
- Repository locale: `C:\Users\Erry\Documents\AiAgentsFactory`
- Stato git al momento della verifica: clean
- File presenti nel workspace:
  - `AgentFactory.md`
  - `.git/`

## Stato struttura repository

| Percorso | Stato | Note | Prossimo step |
|---|---|---|---|
| `README.md` | Mancante | Previsto nella struttura dichiarata. | Creare quando serve una pagina di ingresso sintetica. |
| `AgentFactory.md` | Esistente | Documento architetturale principale presente. | Usarlo come riferimento per gli standard iniziali. |
| `agents/` | Esistente | Cartella per agenti permanenti creata in Fase 2. | Usare come base per la generazione dei workflow. |
| `agents/factory-intake/` | Esistente | Agente permanente per creare il Project Workspace iniziale da una richiesta grezza. | Usare per nuovi progetti. |
| `agents/factory-host/` | Esistente | Coordinatore conversazionale per eseguire piu fasi e Agent Package nella stessa chat. | Usare con `runtime-adapters/codex-conversation.md`. |
| `agents/factory-runner/` | Esistente | Runner a stato macchina per ridurre inferenza e token di contesto. | Usare con `factory-state.json` nei nuovi progetti. |
| `agents/context-compiler/` | Esistente | Agente operativo per compilare contesto minimo da state, summaries e runtime packet. | Usare prima di chiamare runtime AI. |
| `agents/requirement-analyst/` | Esistente | Produce Requirements Blueprint conforme allo standard. | Validare nella prima esecuzione pilota. |
| `agents/architect/` | Esistente | Produce Solution Blueprint conforme allo standard. | Validare nella prima esecuzione pilota. |
| `agents/pipeline-designer/` | Esistente | Produce Execution Blueprint conforme allo standard. | Validare nella prima esecuzione pilota. |
| `agents/pipeline-supervisor/` | Esistente | Verifica processo, handoff e review gate. | Validare nella prima esecuzione pilota. |
| `agents/knowledge-evolution/` | Esistente | Valuta Knowledge Candidate senza integrazione automatica. | Validare dopo la prima esecuzione pilota. |
| `agents/knowledge-compiler/` | Esistente | Incluso esplicitamente per chiudere la lacuna tra flusso e struttura di esempio. | Usare dopo la creazione degli archetype. |
| `archetypes/` | Esistente | Cartella per archetype riutilizzabili creata in Fase 3. | Validare durante generazione Agent Package. |
| `archetypes/developer.md` | Esistente | Archetype MVP previsto. | Validare nella prima esecuzione pilota. |
| `archetypes/tester.md` | Esistente | Archetype MVP previsto. | Validare nella prima esecuzione pilota. |
| `archetypes/reviewer.md` | Esistente | Archetype MVP previsto. | Validare nella prima esecuzione pilota. |
| `archetypes/security-auditor.md` | Esistente | Archetype MVP previsto. | Validare quando serve un gate sicurezza. |
| `archetypes/documentation-writer.md` | Esistente | Archetype MVP previsto. | Validare quando serve documentazione. |
| `capabilities/` | Esistente | Cartella per conoscenza tecnica riutilizzabile creata in Fase 4. | Validare durante generazione Agent Package. |
| `capabilities/git-workflow.md` | Esistente | Capability trasversale per repository Git. | Usare nei task con modifiche versionate. |
| `capabilities/code-review.md` | Esistente | Capability trasversale per review tecnica. | Usare con Reviewer. |
| `capabilities/testing-strategy.md` | Esistente | Capability trasversale per verifiche e test. | Usare con Developer, Tester e Reviewer. |
| `capabilities/node.md` | Esistente | Capability citata nella struttura di esempio. | Usare nei progetti Node. |
| `capabilities/java.md` | Mancante | Capability citata nella struttura di esempio. | Rinviare se non necessaria al primo progetto pilota. |
| `capabilities/postgres.md` | Mancante | Capability citata nella struttura di esempio. | Rinviare se non necessaria al primo progetto pilota. |
| `capabilities/docker.md` | Mancante | Capability citata nella struttura di esempio. | Rinviare se non necessaria al primo progetto pilota. |
| `capabilities/react.md` | Esistente | Capability citata nella struttura di esempio. | Usare nei progetti React. |
| `capabilities/api-security.md` | Esistente | Capability trasversale per API HTTP e sicurezza applicativa. | Usare con Security Auditor o Reviewer. |
| `capabilities/documentation.md` | Esistente | Capability trasversale per documentazione operativa. | Usare con Documentation Writer. |
| `standards/` | Esistente | Cartella centrale per i contratti degli artefatti creata in Fase 1. | Mantenere gli standard come contratti vivi. |
| `standards/agent-package-standard.md` | Esistente | Contratto centrale tra Knowledge Compiler, Agent Package e Runtime Adapter. Supporta sorgente da archetype o definizione ad hoc. | Usare per generare Agent Package. |
| `standards/factory-state-standard.md` | Esistente | Contratto per `factory-state.json`, lo stato macchina compatto del Project Workspace. | Usare per ripresa ed esecuzione elegante. |
| `standards/runtime-packet-standard.md` | Esistente | Contratto per contesto operativo compresso degli agenti temporanei. | Usare dopo Knowledge Compiler. |
| `standards/run-record-standard.md` | Esistente | Contratto per audit record di approval, validazioni, execution e review. | Usare per ogni azione operativa rilevante. |
| `standards/project-bootstrap-standard.md` | Esistente | Contratto per bootstrap automatico di un nuovo Project Workspace. | Usare con Factory Intake. |
| `standards/handoff-standard.md` | Esistente | Contratto minimo per passaggi tra agenti o fasi. | Usare per Execution Blueprint e agenti permanenti. |
| `standards/human-gate-standard.md` | Esistente | Contratto per validazioni umane bloccanti. | Usare in Execution Blueprint, Pipeline Supervisor e runtime adapter. |
| `standards/capability-standard.md` | Esistente | Contratto per capability operative riutilizzabili. | Usare in Fase 4. |
| `standards/requirements-blueprint-standard.md` | Esistente | Contratto per output del Requirement Analyst. | Usare in Fase 2. |
| `standards/solution-blueprint-standard.md` | Esistente | Contratto per output dell'Architect. | Usare in Fase 2. |
| `standards/execution-blueprint-standard.md` | Esistente | Contratto per output del Pipeline Designer. | Usare in Fase 2. |
| `standards/knowledge-candidate-standard.md` | Esistente | Contratto per proposte di evoluzione controllata della conoscenza. | Usare in Fase 2 e Fase 7. |
| `runtime-adapters/` | Esistente | Cartella per traduzione verso runtime specifici creata in Fase 5. | Estendere solo dopo la prima esecuzione manuale. |
| `runtime-adapters/manual-execution.md` | Esistente | Adapter per eseguire Agent Package senza orchestratore automatico. | Usare nella prima esecuzione pilota. |
| `runtime-adapters/codex.md` | Esistente | Adapter per trasformare Agent Package in sessioni Codex ripetibili. | Usare per i prossimi run agentici. |
| `runtime-adapters/codex-project-bootstrap.md` | Esistente | Adapter prompt per avviare un nuovo progetto da una richiesta utente grezza. | Usare prima del Requirement Analyst. |
| `runtime-adapters/codex-conversation.md` | Esistente | Adapter conversazionale per far procedere AgentFactory nella stessa chat con Human Gate inline. | Usare per flussi piu autonomi. |
| `runtime-adapters/claude-code.md` | Mancante | Adapter citato nella struttura di esempio. | Rinviare. |
| `runtime-adapters/opencode.md` | Mancante | Adapter citato nella struttura di esempio. | Rinviare. |
| `runtime-adapters/openai-agents-sdk.md` | Mancante | Adapter citato nella struttura di esempio. | Rinviare. |
| `runtime-adapters/langgraph.md` | Mancante | Adapter citato nella struttura di esempio. | Rinviare. |
| `projects/` | Esistente | Cartella per workspace temporanei di progetto creata in Fase 6. | Usare per la prima esecuzione pilota. |
| `projects/_template/` | Esistente | Template operativo per progetti con input, blueprint, generated-agents, handoff, human-gates, deliverable, reviews e knowledge-candidates. | Copiare per creare il primo progetto pilota. |
| `tools/factory.py` | Esistente | CLI deterministica per start, next action, validate, packet display e approval bookkeeping. | Estendere verso `codex exec` solo dopo validazione. |
| `tools/factory.cmd` | Esistente | Wrapper Windows per usare la CLI anche quando `python` non e nel PATH. | Usare su Windows. |
| `tools/factory.ps1` | Esistente | Wrapper PowerShell alternativo, soggetto a execution policy locale. | Usare solo se consentito. |

## Stato MVP

| MVP | Stato | Evidenza | Prossimo step |
|---|---|---|---|
| MVP 1 - Standardizzazione | Completato | Gli standard minimi, incluso Human Gate Standard, sono presenti in `standards/`. | Validare durante la prima esecuzione pilota. |
| MVP 2 - Agenti permanenti | Completato | I sei agenti permanenti principali sono presenti in `agents/`. | Validare durante la prima esecuzione pilota. |
| MVP 3 - Subagenti temporanei | Completato | I cinque archetype MVP sono presenti in `archetypes/`. | Validare con Knowledge Compiler e prima esecuzione pilota. |
| MVP 4 - Prima esecuzione manuale | Pronto per pilota | Adapter manuale e project template presenti; manca il primo progetto pilota. | Creare un progetto piccolo da eseguire manualmente. |

## Osservazioni

1. Il repository e' attualmente una baseline architetturale: contiene il documento guida, ma non ancora gli artefatti operativi.
2. `AgentFactory.md` cita `Knowledge Compiler` come agente permanente e nel flusso end-to-end, ma la struttura di esempio non include `agents/knowledge-compiler/`. Conviene includerlo esplicitamente nella Fase 2 per evitare una lacuna strutturale.
3. La Fase 1 ha creato i contratti minimi per Agent Package, handoff, blueprint, capability e Knowledge Candidate.
4. La Fase 2 ha creato agenti permanenti con input, output, limiti, workflow e Definition of Done collegati agli standard.
5. Il flusso e stato corretto per supportare agenti temporanei da archetype esistenti o da definizioni ad hoc nell'Execution Blueprint.
6. La Fase 3 ha creato archetype iniziali come conoscenza riutilizzabile, non come lista chiusa dei soli agenti possibili.
7. La Fase 4 ha creato capability iniziali trasversali e tecniche conformi al Capability Standard.
8. Gli Human Gate sono stati introdotti come punti bloccanti di validazione umana, con standard dedicato e integrazione in Execution Blueprint, Pipeline Designer e Pipeline Supervisor.
9. La Fase 5 ha creato il Manual Execution Adapter per eseguire Agent Package con controllo Human Gate, handoff e Knowledge Candidate.
10. La Fase 6 ha creato il Project Workspace Template con struttura tracciabile e regole minime per ogni cartella.
11. Il Codex Runtime Adapter definisce prompt, preflight, Human Gate handling e output finali per eseguire un Agent Package in una chat Codex.
12. Factory Intake e Codex Project Bootstrap permettono di partire da una sola idea utente creando workspace e primo Agent Package senza bootstrap manuale.
13. Factory Host e Codex Conversation Adapter permettono di coordinare piu agenti e Human Gate nella stessa chat, riducendo il passaggio manuale di prompt.
14. Il pilot end-to-end ora richiede quattro approval espliciti: requisiti, architettura, piano/team agenti e lavoro finito.
15. Factory Runner, Factory State e Runtime Packet introducono una modalita piu elegante e token-efficient: stato macchina compatto, summaries approvate e contesto minimo per agente.
16. La Fase 9 introduce Operational Runner: Context Compiler, Run Record Standard e CLI minima `tools/factory.py` per spostare bootstrap, validazioni e approval bookkeeping fuori dal modello AI.

## Prossimo step consigliato

Usare Factory Host + Factory Runner per avviare o riprendere progetti in modalita conversazionale:

```text
runtime-adapters/codex-conversation.md
agents/factory-runner/factory-runner.md
```

Criterio di completamento del prossimo step: una richiesta utente deve poter avanzare nella stessa chat attraverso `factory-state.json`, blueprint, Human Gate, summaries, runtime packet, Agent Package temporanei, execution e review.

Comandi operativi minimi:

```text
python tools/factory.py start "<idea>" --project-id <project-id>
python tools/factory.py next projects/<project-id>
python tools/factory.py validate projects/<project-id>
python tools/factory.py packet projects/<project-id> <packet-id>
python tools/factory.py approve projects/<project-id> <gate-id> --decision Approved
```

Su Windows:

```text
tools\factory.cmd start "<idea>" --project-id <project-id>
tools\factory.cmd next projects\<project-id>
tools\factory.cmd validate projects\<project-id>
tools\factory.cmd packet projects\<project-id> <packet-id>
tools\factory.cmd approve projects\<project-id> <gate-id> --decision Approved
```

Per la prova reale CeraMirycs usare:

```text
runbooks/ceramirycs-real-pilot.md
```
