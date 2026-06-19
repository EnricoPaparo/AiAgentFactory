# Tools e Function Calling

## Come funziona il Function Calling

Il **Function Calling** (o Tool Use) è il meccanismo con cui un LLM può richiedere l'esecuzione di funzioni esterne.

Il flusso è:

```
1. Definisci gli strumenti disponibili nel prompt/API
2. L'LLM decide SE e QUALE strumento usare
3. L'LLM genera i parametri da passare allo strumento
4. Il tuo codice esegue la funzione
5. Il risultato viene restituito all'LLM
6. L'LLM genera la risposta finale
```

Il modello **non esegue** il codice — genera solo JSON con i parametri. Sei tu a eseguire la funzione e a restituire il risultato.

---

## Definire uno strumento con Claude API

```python
import anthropic

client = anthropic.Anthropic()

# Definizione dello strumento
tools = [
    {
        "name": "get_weather",
        "description": "Ottieni le condizioni meteo attuali per una città",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nome della città (es. 'Roma', 'Milano')"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Unità di misura della temperatura"
                }
            },
            "required": ["city"]
        }
    }
]

# Prima chiamata: il modello decide se usare il tool
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "Che tempo fa a Roma oggi?"}
    ]
)
```

---

## Gestire la risposta del tool

```python
import json

# Il modello risponde con una richiesta di tool use
if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    
    tool_name = tool_use.name          # "get_weather"
    tool_input = tool_use.input        # {"city": "Roma", "unit": "celsius"}
    
    # Esegui la funzione reale
    result = get_weather(tool_input["city"], tool_input.get("unit", "celsius"))
    
    # Restituisci il risultato al modello
    final_response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "Che tempo fa a Roma oggi?"},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": json.dumps(result)
                    }
                ]
            }
        ]
    )
    
    print(final_response.content[0].text)
```

---

## Loop di esecuzione automatica

In un agente reale, il tool calling avviene in loop finché il modello non è soddisfatto:

```python
def run_agent(user_message: str, tools: list, tool_handlers: dict) -> str:
    messages = [{"role": "user", "content": user_message}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )
        
        # Risposta finale — nessun tool da chiamare
        if response.stop_reason == "end_turn":
            return response.content[0].text
        
        # Il modello vuole usare uno o più tool
        if response.stop_reason == "tool_use":
            # Aggiungi risposta del modello alla storia
            messages.append({"role": "assistant", "content": response.content})
            
            # Esegui tutti i tool richiesti
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    handler = tool_handlers[block.name]
                    result = handler(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })
            
            # Aggiungi i risultati e continua il loop
            messages.append({"role": "user", "content": tool_results})
```

---

## Strumenti pratici da implementare

### Ricerca web

```python
def search_web(query: str, num_results: int = 5) -> list[dict]:
    """Cerca su web e restituisce titoli + snippet + URL"""
    # Usa SerpAPI, Brave Search API, o Tavily
    import tavily
    results = tavily.search(query, max_results=num_results)
    return [{"title": r.title, "url": r.url, "snippet": r.content} 
            for r in results.results]
```

### Esecuzione codice Python

```python
import subprocess
import tempfile

def execute_python(code: str) -> dict:
    """Esegue codice Python in sandbox e restituisce output"""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w") as f:
        f.write(code)
        f.flush()
        result = subprocess.run(
            ["python", f.name],
            capture_output=True, text=True, timeout=30
        )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
```

### Query database

```python
import sqlite3

def query_database(sql: str) -> list[dict]:
    """Esegue una SELECT sul database e restituisce i risultati"""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(sql)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results
```

---

## Best practice per la definizione dei tool

### Nomi e descrizioni chiari

```python
# ❌ Vago
{"name": "do_thing", "description": "Fa qualcosa"}

# ✅ Specifico
{"name": "send_slack_message", 
 "description": "Invia un messaggio a un canale Slack specifico. Usa questo tool quando vuoi notificare il team di un aggiornamento."}
```

### Schema preciso

```python
"input_schema": {
    "type": "object",
    "properties": {
        "channel": {
            "type": "string",
            "description": "Nome del canale Slack SENZA il #, es. 'general', 'team-dev'"
        },
        "message": {
            "type": "string", 
            "description": "Testo del messaggio da inviare"
        },
        "urgent": {
            "type": "boolean",
            "description": "Se true, invia anche una notifica push al team",
            "default": False
        }
    },
    "required": ["channel", "message"]
}
```

---

## Gestione degli errori

```python
def safe_tool_call(handler, **kwargs):
    try:
        result = handler(**kwargs)
        return {"success": True, "result": result}
    except ValueError as e:
        return {"success": False, "error": f"Parametri non validi: {e}"}
    except TimeoutError:
        return {"success": False, "error": "Timeout: l'operazione ha impiegato troppo tempo"}
    except Exception as e:
        return {"success": False, "error": f"Errore inaspettato: {type(e).__name__}: {e}"}
```

Restituisci sempre errori strutturati — il modello può decidere di riprovare o cambiare strategia.

---

## Tool calling parallelo

Claude può chiamare più tool in parallelo quando sono indipendenti:

```
Utente: "Confronta il meteo di Roma, Milano e Napoli"

Claude chiama in parallelo:
  - get_weather("Roma")
  - get_weather("Milano") 
  - get_weather("Napoli")
```

Questo riduce la latenza totale. Assicurati che il tuo loop gestisca più `tool_use` nella stessa risposta.

Nel prossimo modulo costruiamo il cuore dei sistemi di conoscenza degli agenti: il **RAG**.
