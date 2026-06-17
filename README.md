# AISA — AISolutionArchitect

Dai un'idea in qualsiasi formato. Ricevi tre documenti professionali:
**Analisi dei Requisiti · Architettura · Piano di Implementazione**

---

## Avvio rapido

**Prerequisiti:** Python 3.11+, API key Anthropic

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

```bash
# Da descrizione testuale
python tools/run.py "descrizione del progetto"

# Con file di input (testo, PDF, DOCX, immagini)
python tools/run.py "descrizione" --files ./miei-documenti/

# Con revisione interattiva tra ogni step
python tools/run.py "descrizione" --files ./docs/ --review

# Anteprima senza eseguire
python tools/run.py "descrizione" --dry-run
```

I documenti vengono salvati in `projects/<nome-progetto>/documents/`.

---

## Output

| Documento | Contenuto |
|---|---|
| `requirements.md` | Executive summary, requisiti funzionali/non funzionali, vincoli, rischi, matrice di complessità |
| `architecture.md` | Decisioni architetturali, stack motivato, componenti, flussi, sicurezza, scalabilità |
| `implementation-plan.md` | Moduli, dipendenze, fasi, percorso critico, stime effort, raccomandazioni MVP |

---

## Struttura

```
AISA/
├── agents/
│   ├── requirement-analyst/   # Analisi requisiti enterprise
│   ├── architect/             # Architettura motivata
│   └── implementation-planner/ # Piano di implementazione
├── standards/                 # Struttura attesa dei documenti
├── tools/
│   ├── run.py                 # Entry point unico
│   └── pdf.py                 # Generazione PDF (Fase 2)
├── web/                       # Portale web (Fase 4)
├── projects/                  # Workspace per progetto
└── requirements.txt
```

---

## Opzioni

```
python tools/run.py "descrizione" [opzioni]

  --files, -f    PERCORSO   file o cartella con materiali di input
  --project-id   ID         nome workspace (default: auto-generato)
  --model, -m    MODELLO    modello AI (default: claude-opus-4-8)
  --review                  gate di revisione interattivo tra ogni step
  --dry-run                 anteprima senza chiamate API
  --force                   sovrascrive workspace esistente
```
