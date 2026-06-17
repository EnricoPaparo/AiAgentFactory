---
standard: archetype
applies-to: "archetypes/*.md"
required-sections:
  - "## Scopo"
  - "## Natura Dell'Archetype"
  - "## Responsabilita"
  - "## Input Attesi"
  - "## Output Attesi"
  - "## Limiti"
  - "## Capability Compatibili"
  - "## Handoff Richiesto"
  - "## Definition Of Done"
  - "## Failure Mode Da Evitare"
optional-sections: []
---

# Archetype Standard

## Scopo

Definire il formato minimo di un archetype. Un archetype e uno scheletro riutilizzabile e approvato per generare subagenti temporanei di un tipo ricorrente. Definisce ruolo, responsabilita, input, output, limiti e formato dei deliverable — senza contenere conoscenza tecnica specifica (quella appartiene alle capability) e senza limitare la creazione di agenti ad hoc.

## Creato da

Knowledge Evolution o maintainer della factory, dopo validazione che il ruolo sia genuinamente ricorrente tra progetti diversi.

## Usato da

Knowledge Compiler, Pipeline Designer, Pipeline Supervisor.

## Quando si usa

Si usa quando un ruolo di subagente temporaneo si e dimostrato ricorrente in piu progetti e merita stabilizzazione come conoscenza riutilizzabile. Un archetype non sostituisce gli agenti ad hoc: e una base, non un vincolo.

## Campi obbligatori

| Campo | Descrizione |
|---|---|
| `Scopo` | A cosa serve l'archetype — tipo di task che copre. |
| `Natura Dell'Archetype` | Chiarisce che l'archetype e conoscenza riutilizzabile, non lista chiusa dei soli agenti possibili. |
| `Responsabilita` | Cosa fa l'agente generato da questo archetype. |
| `Input Attesi` | Artefatti e file che l'agente deve ricevere per operare. |
| `Output Attesi` | Deliverable che l'agente deve produrre. |
| `Limiti` | Cosa l'agente non deve fare — confini operativi espliciti. |
| `Capability Compatibili` | Tipi di capability che possono essere assegnate a questo ruolo. |
| `Handoff Richiesto` | Contenuto minimo dell'handoff che l'agente deve produrre. |
| `Definition Of Done` | Condizioni verificabili di completamento del task. |
| `Failure Mode Da Evitare` | Errori ricorrenti specifici a questo tipo di agente. |

## Campi opzionali

Nessun campo opzionale definito. La struttura degli archetype e intenzionalmente uniforme per garantire che il Knowledge Compiler possa comporre Agent Package in modo prevedibile.

## Formato consigliato

```markdown
# Archetype: <NomeRuolo>

## Scopo

## Natura Dell'Archetype

## Responsabilita

## Input Attesi

## Output Attesi

## Limiti

## Capability Compatibili

## Handoff Richiesto

## Definition Of Done

## Failure Mode Da Evitare
```

## Criteri di validita

Un archetype e valido quando:

1. il ruolo e genuinamente ricorrente — non e una specializzazione per un singolo progetto;
2. non contiene conoscenza tecnica specifica (quella va nelle capability);
3. i limiti prevengono sovrapposizioni con altri archetype;
4. le capability compatibili sono tipi, non istanze — l'archetype non prescrive quale specifica capability usare;
5. l'handoff richiesto e verificabile dal Pipeline Supervisor;
6. la Definition of Done non dipende da contesto di progetto specifico;
7. i failure mode sono ricorrenti tra progetti, non specifici a un caso.

## Differenza Tra Archetype E Agente Ad Hoc

| | Archetype | Agente ad hoc |
|---|---|---|
| **Quando nasce** | Dopo validazione di ricorrenza tra progetti | Nell'Execution Blueprint di un progetto specifico |
| **Vive in** | `archetypes/` (conoscenza permanente) | `projects/<id>/blueprints/execution-blueprint.md` |
| **Chi lo crea** | Knowledge Evolution + maintainer | Pipeline Designer |
| **Requisito** | Dimostrata riutilizzabilita | Necessita specifica del progetto |
| **Puo diventare archetype** | Gia e archetype | Si, tramite Knowledge Candidate |

Un agente ad hoc che si dimostra utile in piu progetti genera una Knowledge Candidate per creare un nuovo archetype. Questa e la via corretta — non creare archetype per ipotesi.

## Failure mode

- Archetype troppo specifico — contiene conoscenza valida solo per un progetto.
- Archetype che duplica un archetype esistente con nome diverso.
- Capability tecniche specifiche incluse nell'archetype invece che nelle capability assegnate.
- Handoff richiesto vago o non verificabile.
- Definition of Done dipendente da contesto di progetto non portabile.
- Archetype creato senza evidenza di ricorrenza tra piu progetti.
- Failure mode generici non collegati al tipo di agente.

## Esempio minimo

```markdown
# Archetype: Security Auditor

## Scopo

Modello riutilizzabile per generare agenti temporanei che eseguono
audit di sicurezza su codice, configurazioni e architetture.

## Natura Dell'Archetype

Questo archetype stabilizza il ruolo Security Auditor per review di sicurezza
ricorrenti. Non impedisce al Pipeline Designer di definire ruoli di audit
piu specializzati ad hoc quando necessario.

## Responsabilita

- Analizzare il perimetro assegnato per vulnerabilita e rischi di sicurezza.
- Produrre un report con problemi, severita e raccomandazioni.
- Distinguere rischi bloccanti da rischi accettabili con mitigazione.

## Input Attesi

- Agent Package conforme a `standards/agent-package-standard.md`.
- Artefatti da auditare (codice, configurazioni, architettura).
- Blueprint rilevanti.
- Capability di sicurezza assegnate.

## Output Attesi

- Security audit report con problemi, severita e raccomandazioni.
- Esito: approved, changes required o blocked.
- Eventuali Knowledge Candidate su vulnerability pattern nuovi.

## Limiti

- Non implementa correzioni salvo incarico esplicito.
- Non sostituisce penetration test o audit di compliance formale.
- Non approva senza evidenza di analisi effettiva.
- Non allarga il perimetro oltre l'Agent Package.

## Capability Compatibili

- Capability di sicurezza applicativa.
- Capability di revisione configurazioni.
- Capability di analisi architetturale.

## Handoff Richiesto

Il Security Auditor deve consegnare almeno:

- perimetro analizzato;
- problemi rilevati con severita;
- evidenza per ogni problema;
- raccomandazioni azionabili;
- esito del gate.

## Definition Of Done

- Il perimetro dichiarato nell'Agent Package e stato analizzato.
- I problemi sono concreti, azionabili e ordinati per severita.
- L'esito e chiaro e non ambiguo.
- L'handoff e conforme allo standard.

## Failure Mode Da Evitare

- Report generico senza evidenza specifica.
- Allargare il perimetro oltre l'Agent Package.
- Approvare senza analisi effettiva.
- Confondere best practice con vulnerabilita concrete.
```
