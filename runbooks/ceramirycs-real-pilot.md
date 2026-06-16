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

## Prompt Breve Da Usare In Una Nuova Chat Codex

Prima puoi creare il workspace deterministico con:

```text
tools\factory.cmd start "Voglio creare un sito web minimale e semplicissimo per Miriam e le sue produzioni di ceramica cozy. L'attivita si chiama CeraMirycs. Il sito deve essere moderno, caldo, artigianale e pulito. Bastano una landing page e una pagina contatti. I veri contatti devono restare vuoti o indicati come da definire: email, telefono, indirizzo e Instagram. Non inventare dati di contatto realistici." --project-id ceramirycs
```

Poi usa il prompt creato in:

```text
projects\ceramirycs\run-records\next-requirement-analyst-prompt.md
```

```text
Esegui AgentFactory su questa idea:
Voglio creare un sito web minimale e semplicissimo per Miriam e le sue produzioni di ceramica cozy.
L'attivita si chiama CeraMirycs.
Il sito deve essere moderno, caldo, artigianale e pulito.
Bastano una landing page e una pagina contatti.
I veri contatti devono restare vuoti o indicati come "da definire": email, telefono, indirizzo e Instagram.
Non inventare dati di contatto realistici.

Repository:
C:\Users\Erry\Documents\AiAgentsFactory

Regole:
- Usa Factory Host, Factory Runner e Codex Conversation Adapter.
- Parti da zero: se esiste gia un workspace CeraMirycs precedente, fermati e segnala il conflitto invece di riusarlo.
- Mantieni tutto nella stessa chat.
- Crea o aggiorna factory-state.json.
- Usa tools/factory.py per validare stato, mostrare next action e gestire approval se appropriato.
- Produci gli artefatti fase per fase dentro projects/<project-id>/.
- Usa almeno questi Human Gate: approve-requirements, approve-solution-blueprint, approve-execution-plan, approve-final-delivery.
- Dopo ogni Human Gate Pending, fermati e chiedimi Approved / Changes Requested / Rejected.
- Dopo approval, aggiorna il file del gate e prosegui con la fase successiva.
- Non saltare Requirement Analyst, Architect, Pipeline Designer o Knowledge Compiler.
- Il Pipeline Designer puo creare agenti temporanei ad hoc se non esiste un archetype adatto.
- Crea Agent Package temporanei e runtime packet quando il progetto arriva alla fase operativa.
- Usa summaries e runtime packet per ridurre il contesto degli agenti temporanei.
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
