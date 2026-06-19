# Agenti AI: Architettura e Componenti

## Da LLM ad Agente

Un LLM da solo genera testo. Un **agente AI** usa un LLM come "cervello" e aggiunge:

- **Memoria** — ricorda il passato
- **Strumenti** — può agire nel mondo
- **Pianificazione** — divide obiettivi complessi in passi
- **Loop autonomo** — lavora fino al completamento del task

```
         ┌─────────────────────────────────────┐
         │           AGENTE AI                 │
         │                                     │
Input ──►│  LLM (ragionamento)                 │──► Output
         │   ├── Memoria                       │
         │   ├── Strumenti (Tools)             │
         │   └── Pianificazione               │
         └─────────────────────────────────────┘
```

---

## Il ciclo ReAct

**ReAct** (Reasoning + Acting) è il pattern fondamentale degli agenti:

```
PENSIERO (Thought): Devo trovare il prezzo del prodotto X
AZIONE (Action):    search_web("prezzo prodotto X")
OSSERVAZIONE (Obs): "Il prodotto X costa €49.99 su Amazon"
PENSIERO:           Ho il prezzo. Ora devo confrontarlo con il budget.
AZIONE:             compare_price(49.99, budget=100)
OSSERVAZIONE:       "Rientra nel budget"
RISPOSTA FINALE:    Il prodotto X a €49.99 rientra nel budget di €100.
```

Il modello alterna ragionamento e azioni fino a trovare la risposta. Questo loop è la spina dorsale di quasi tutti gli agenti.

---

## I tipi di memoria

### Memoria in-context
Tutto ciò che sta nella conversazione corrente. Veloce, ma limitata dalla context window.

```python
messages = [
  {"role": "user",      "content": "Mi chiamo Marco"},
  {"role": "assistant", "content": "Ciao Marco!"},
  {"role": "user",      "content": "Come mi chiamo?"},  # sa la risposta
]
```

### Memoria esterna (episodica)
Un database dove l'agente salva e recupera informazioni tra sessioni diverse.

```python
# Salva dopo ogni conversazione
memory_db.save(user_id="marco", fact="preferisce risposte brevi")

# Recupera all'inizio della sessione successiva
context = memory_db.get(user_id="marco")
```

### Memoria semantica
Embedding di documenti, FAQ, knowledge base — recuperati con ricerca semantica.

### Memoria procedurale
"Come fare le cose" — runbook, istruzioni, workflow salvati e richiamati dall'agente.

---

## I tipi di strumenti (Tools)

Gli strumenti sono funzioni che l'agente può chiamare:

### Ricerca e informazioni
- `search_web(query)` — cerca su internet
- `query_database(sql)` — interroga un DB
- `read_file(path)` — legge un file

### Azioni nel mondo
- `send_email(to, subject, body)` — invia email
- `create_issue(title, body)` — crea un ticket
- `book_meeting(date, participants)` — prenota una riunione

### Codice e calcoli
- `execute_python(code)` — esegue codice Python
- `calculate(expression)` — calcoli matematici

### API esterne
- `get_weather(city)` — meteo
- `translate(text, lang)` — traduzione
- Qualsiasi API REST

---

## Pianificazione

Gli agenti complessi **pianificano** prima di agire:

### Plan-and-Execute
```
Obiettivo: "Analizza le vendite Q3 e prepara un report per il board"

Piano:
1. Recupera i dati di vendita da luglio ad agosto dal database
2. Calcola totali, trend e confronto con Q3 anno precedente
3. Identifica i top 5 prodotti per fatturato
4. Genera grafici
5. Scrivi il report in formato PowerPoint

Esecuzione: [step 1] → [step 2] → ... → [report finale]
```

### Riflessione e correzione
Gli agenti avanzati valutano i propri risultati intermedi e correggono il piano se necessario.

---

## Architetture di agenti

### Agente singolo (Single Agent)
Un LLM con strumenti. Ottimo per task mediamente complessi.

```
Utente → Agente → [usa tools] → Risposta
```

### Pipeline sequenziale
Una catena di agenti dove l'output di uno è l'input del successivo.

```
Agente1 (scraper) → Agente2 (analisi) → Agente3 (report)
```

### Orchestratore + Sub-agenti
Un orchestratore centrale coordina agenti specializzati.

```
           ┌─────────────────┐
           │  ORCHESTRATORE  │
           └────────┬────────┘
          ┌─────────┼─────────┐
     ┌────▼───┐ ┌───▼────┐ ┌──▼─────┐
     │Research│ │Analyst │ │Writer  │
     └────────┘ └────────┘ └────────┘
```

---

## Livelli di autonomia

| Livello | Descrizione | Esempio |
|---------|-------------|---------|
| 0 | Solo LLM, nessuna azione | Chatbot Q&A |
| 1 | LLM + tools semplici | Ricerca web |
| 2 | Loop autonomo + memoria | Agente ricerca |
| 3 | Multi-step planning | Agente developer |
| 4 | Multi-agente collaborativo | Team AI |
| 5 | Auto-miglioramento | Ancora sperimentale |

---

## Human-in-the-Loop

Gli agenti più affidabili includono **checkpoint umani** per azioni critiche:

```python
def agente_ordini():
    ordine = pianifica_ordine(prodotti)
    
    # Gate umano prima di procedere
    if ordine.valore > 10000:
        approvazione = chiedi_approvazione_umana(ordine)
        if not approvazione:
            return "Ordine annullato"
    
    esegui_ordine(ordine)
```

> **Regola d'oro**: più un'azione è irreversibile, più è importante avere un gate umano.

---

## Valutare un agente

Un buon agente deve essere:

- **Accurato**: raggiunge l'obiettivo correttamente
- **Efficiente**: usa il minimo numero di passi
- **Robusto**: gestisce errori e casi limite
- **Sicuro**: non fa azioni pericolose senza conferma
- **Trasparente**: spiega il suo ragionamento

Nel Modulo 5 vedremo come implementare concretamente gli strumenti.
