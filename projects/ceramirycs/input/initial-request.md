# Initial Request

Voglio creare un sito web minimale e semplicissimo per Miriam e le sue produzioni di ceramica cozy.
L'attivita si chiama CeraMirycs.
Il sito deve essere moderno, caldo, artigianale e pulito.
Bastano una landing page e una pagina contatti.
I veri contatti devono restare vuoti o indicati come "da definire": email, telefono, indirizzo e Instagram.
Non inventare dati di contatto realistici.

Regole operative AgentFactory:

- Parti da zero: se esiste gia un workspace CeraMirycs precedente, fermati e segnala il conflitto invece di riusarlo.
- Mantieni tutto nella stessa chat.
- Se non esiste un Project Workspace, avvia Factory Intake.
- Produci gli artefatti fase per fase dentro `projects/<project-id>/`.
- Usa almeno questi Human Gate: `approve-requirements`, `approve-solution-blueprint`, `approve-execution-plan`, `approve-final-delivery`.
- Dopo ogni Human Gate Pending, fermati e chiedimi Approved / Changes Requested / Rejected.
- Dopo approval, aggiorna il file del gate e prosegui con la fase successiva.
- Non saltare Requirement Analyst, Architect, Pipeline Designer o Knowledge Compiler.
- Il Pipeline Designer puo creare agenti temporanei ad hoc se non esiste un archetype adatto.
- Crea ed esegui Agent Package temporanei quando il progetto arriva alla fase operativa.
- Ogni fase deve riepilogare file creati/modificati, verifiche fatte, gate aperti e prossimo passo.
- Alla fine del lavoro, esegui review e Pipeline Supervisor prima di chiedere `approve-final-delivery`.
