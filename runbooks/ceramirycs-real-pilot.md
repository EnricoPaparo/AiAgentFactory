# CeraMirycs Real Pilot

## Scopo

Eseguire una prova reale di AgentFactory in modalita conversazionale, partendo da una sola idea utente e lasciando che la factory crei il Project Workspace, i blueprint, il team temporaneo di agenti, i deliverable e le review.

Questa prova deve verificare soprattutto il flusso degli Human Gate, non solo la produzione del sito.

## Gate Di Approval Previsti

| Gate | Cosa approvi | Quando blocca |
|---|---|---|
| `approve-requirements` | Requisiti del sito e vincoli sui contatti vuoti. | Prima dell'architettura. |
| `approve-solution-blueprint` | Architettura, stack, struttura pagine, rischi e trade-off. | Prima del piano operativo. |
| `approve-execution-plan` | Team di agenti temporanei, workflow, handoff e review. | Prima della generazione/esecuzione degli Agent Package operativi. |
| `approve-final-delivery` | Lavoro finito dopo review e verifica del Pipeline Supervisor. | Prima della chiusura. |

## Prompt Da Usare In Una Nuova Chat Codex

```text
Esegui AgentFactory in modalita conversazionale usando Codex Conversation Adapter.

Repository:
C:\Users\Erry\Documents\AiAgentsFactory

Factory Host:
agents/factory-host/factory-host.md

Conversation adapter:
runtime-adapters/codex-conversation.md

Single-agent adapter:
runtime-adapters/codex.md

Manual adapter base:
runtime-adapters/manual-execution.md

Richiesta utente:
Voglio creare un sito web minimale e semplicissimo per Miriam e le sue produzioni di ceramica cozy.
L'attivita si chiama CeraMirycs.
Il sito deve essere moderno, caldo, artigianale e pulito.
Bastano una landing page e una pagina contatti.
I veri contatti devono restare vuoti o indicati come "da definire": email, telefono, indirizzo e Instagram.
Non inventare dati di contatto realistici.

Regole:
- Parti da zero: se esiste gia un workspace CeraMirycs precedente, fermati e segnala il conflitto invece di riusarlo.
- Mantieni tutto nella stessa chat.
- Se non esiste un Project Workspace, avvia Factory Intake.
- Produci gli artefatti fase per fase dentro projects/<project-id>/.
- Usa almeno questi Human Gate: approve-requirements, approve-solution-blueprint, approve-execution-plan, approve-final-delivery.
- Dopo ogni Human Gate Pending, fermati e chiedimi Approved / Changes Requested / Rejected.
- Dopo approval, aggiorna il file del gate e prosegui con la fase successiva.
- Non saltare Requirement Analyst, Architect, Pipeline Designer o Knowledge Compiler.
- Il Pipeline Designer puo creare agenti temporanei ad hoc se non esiste un archetype adatto.
- Crea ed esegui Agent Package temporanei quando il progetto arriva alla fase operativa.
- Ogni fase deve riepilogare file creati/modificati, verifiche fatte, gate aperti e prossimo passo.
- Alla fine del lavoro, esegui review e Pipeline Supervisor prima di chiedere approve-final-delivery.
```

## Come Valutare La Prova

La prova e valida se:

1. nasce un nuovo workspace sotto `projects/`;
2. la richiesta originale viene salvata in `input/initial-request.md`;
3. Codex si ferma davvero sui quattro gate;
4. l'architettura non viene scelta prima dell'approvazione requisiti;
5. il team di agenti non viene generato/eseguito prima dell'approvazione del piano;
6. il sito prodotto non contiene contatti realistici inventati;
7. il lavoro finito passa da review e Pipeline Supervisor prima del gate finale.
