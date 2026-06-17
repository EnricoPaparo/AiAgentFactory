# AiAgentFactory

Repository strutturato di conoscenza per progettare, generare, orchestrare, supervisionare ed evolvere team temporanei di agenti AI specializzati per progetti software.

AiAgentFactory **non è** un runtime, un framework, né una libreria di prompt. È il riferimento architetturale della factory: definisce identità, confini, componenti, workflow, contratti e regole invarianti. Gli standard operativi per i singoli artefatti vivono in `standards/`.

---

## Perché esiste

I grandi progetti software gestiti da agenti AI falliscono in modo prevedibile: responsabilità sovrapposte, handoff mancanti, nessun checkpoint umano, nessuna retention della conoscenza tra una sessione e l'altra. AiAgentFactory risolve questo trattando lo sviluppo basato su agenti come un **processo di fabbrica** — con ruoli di governance permanenti, contratti formali tra agenti, Human Gate decisionali obbligatori e un ciclo controllato di evoluzione della conoscenza.

---

## Come Funziona

```text
Richiesta utente
  → Requirement Analyst       (chiarisce i requisiti)
  → Requirements Blueprint
  → Architect                 (progetta la soluzione)
  → Solution Blueprint
  → Pipeline Designer         (progetta il workflow)
  → Execution Blueprint
  → Knowledge Compiler        (assembla gli Agent Package)
  → Agent Package(s)
  → Runtime Adapter           (traduce nel runtime scelto)
  → Esecuzione del team temporaneo
  → Pipeline Supervisor       (verifica la conformità del processo)
  → Knowledge Evolution       (valuta le proposte di miglioramento)
  → aggiornamento controllato della conoscenza permanente
```

Ogni passo produce un artefatto versionato con proprietario, input, output e Definition of Done espliciti. Nulla avanza senza un handoff verificato. Le decisioni umane vengono imposte tramite Human Gate bloccanti.

---

## Struttura del Repository

```text
AiAgentFactory/
├── AgentFactory.md              # Riferimento architetturale completo (inizia qui)
├── implementation-status.md     # Stato di avanzamento dell'implementazione
│
├── agents/                      # Agenti permanenti della factory (ruoli di governance)
│   ├── requirement-analyst/
│   ├── architect/
│   ├── pipeline-designer/
│   ├── pipeline-supervisor/
│   ├── knowledge-compiler/
│   └── knowledge-evolution/
│
├── archetypes/                  # Template riutilizzabili per agenti temporanei
│   ├── developer.md
│   ├── tester.md
│   ├── reviewer.md
│   ├── security-auditor.md
│   └── documentation-writer.md
│
├── capabilities/                # Pacchetti di conoscenza operativa riutilizzabile
│   └── (emergono da Knowledge Candidate approvate)
│
├── standards/                   # Contratti di formato per tutti gli artefatti
│   ├── agent-package-standard.md
│   ├── handoff-standard.md
│   ├── human-gate-standard.md
│   ├── execution-blueprint-standard.md
│   ├── requirements-blueprint-standard.md
│   ├── solution-blueprint-standard.md
│   ├── capability-standard.md
│   ├── knowledge-candidate-standard.md
│   ├── permanent-agent-standard.md
│   └── archetype-standard.md
│
├── runtime-adapters/            # Regole di traduzione per runtime specifici
│   ├── manual-execution.md
│   ├── claude-code.md
│   ├── opencode.md
│   ├── openai-agents-sdk.md
│   ├── github-actions.md
│   └── langgraph.md
│
├── tools/                       # Strumenti a riga di comando
│   ├── new-project.py           # Crea un nuovo project workspace
│   ├── status.py                # Mostra lo stato di un progetto
│   ├── validate.py              # Valida gli artefatti contro gli standard
│   └── orchestrate.py          # Esegue automaticamente una pipeline di agenti
│
└── projects/                    # Project workspace (temporanei, per progetto)
    └── _template/               # Copiare per iniziare un nuovo progetto
```

**Dove mettere cosa:**

| Tipo di conoscenza | Destinazione |
|---|---|
| Regola di comportamento di un agente permanente | `agents/<nome-agente>/` |
| Template riutilizzabile per agenti temporanei | `archetypes/<ruolo>.md` |
| Conoscenza tecnica riutilizzabile | `capabilities/<argomento>.md` |
| Contratto di formato per un artefatto | `standards/<artefatto>-standard.md` |
| Regole di traduzione per un runtime | `runtime-adapters/<runtime>.md` |
| Lavoro specifico di progetto | `projects/<project-id>/` |
| Proposta di miglioramento (non ancora approvata) | `projects/<project-id>/knowledge-candidates/` |

---

## Avvio Rapido: Nuovo Progetto

**Prerequisiti:** Python 3.11+, `pip install -r requirements.txt`

### Comando unico (consigliato)

```bash
export ANTHROPIC_API_KEY=sk-ant-...

# Con file di input (testo, PDF, DOCX, immagini)
python tools/factory.py run "descrizione del progetto" --files ./miei-documenti/

# Solo da descrizione testuale
python tools/factory.py run "API REST per gestione utenti"

# Con budget massimo e modello specifico
python tools/factory.py run "descrizione" --files ./docs/ --budget 2.00 --model claude-sonnet-4-6

# Anteprima senza eseguire
python tools/factory.py run "descrizione" --dry-run
```

Il comando crea automaticamente il workspace, carica i file, li preprocessa e avvia la pipeline.

### Opzione manuale (OpenCode, Claude Code, ecc.)

```bash
# 1. Crea il workspace
python tools/new-project.py mio-progetto

# 2. Compila projects/mio-progetto/input/initial-request.md

# 3. Apri il runtime scelto e segui il runtime adapter corrispondente
#    Esempio per OpenCode: runtime-adapters/opencode.md
#    Esempio per Claude Code: runtime-adapters/claude-code.md
```

**Rispetta sempre i Human Gate:** qualsiasi file in `human-gates/` con stato `Pending` **blocca** tutte le attività nel suo `blocking-scope`. Non avanzare finché una decisione umana non è registrata.

Consulta `projects/_template/README.md` per la guida completa cartella per cartella.

---

## Documenti Chiave

| Documento | Scopo |
|---|---|
| `AgentFactory.md` | Riferimento architetturale completo — invarianti, concetti, workflow |
| `standards/agent-package-standard.md` | Come costruire un Agent Package valido |
| `standards/handoff-standard.md` | Campi obbligatori per la consegna tra agenti |
| `standards/human-gate-standard.md` | Come definire e imporre i Human Gate |
| `runtime-adapters/manual-execution.md` | Come eseguire la factory senza orchestratore |
| `runtime-adapters/opencode.md` | Come eseguire Agent Package su OpenCode |
| `runtime-adapters/claude-code.md` | Come eseguire Agent Package su Claude Code |
| `CONTRIBUTING.md` | Come estendere la factory (capability, archetype, standard) |
| `GLOSSARY.md` | Definizioni di tutti i termini della factory |

---

## Stato Corrente

Vedi `implementation-status.md` per il tracker dettagliato.

**Riepilogo MVP:**
- MVP 1 (Standard): Completo — 10 contratti di formato definiti con frontmatter YAML
- MVP 2 (Agenti permanenti): Completo — 6 agenti permanenti definiti
- MVP 3 (Archetype): Completo — 5 archetype base definiti
- MVP 4 (Prima esecuzione): Completo — progetto pilota eseguito end-to-end
- Tooling: Completo — `new-project.py`, `status.py`, `validate.py`, `orchestrate.py`

---

## Regole Invarianti

Queste regole valgono indipendentemente da runtime, modello AI o strumenti usati:

1. La conoscenza permanente è il principale asset della factory.
2. Gli agenti temporanei sono usa e getta — creati per progetto, non permanenti.
3. Nessuna proposta generata durante un progetto aggiorna automaticamente la conoscenza permanente.
4. I runtime sono intercambiabili e non devono contenere logica decisionale della factory.
5. Ruoli, responsabilità, contratti e workflow vengono definiti prima dell'esecuzione tecnica.
6. Ogni passo significativo ha input, output, proprietario e criteri di completamento espliciti.
7. Il Project Workspace contiene lavoro temporaneo, non conoscenza approvata.
8. Il Pipeline Supervisor valida la conformità del processo — non è un super-agente onnisciente.
9. Un Human Gate Pending blocca tutte le attività nel suo `blocking-scope` dichiarato.
10. Il codice è uno strumento operativo, non il centro della factory.
