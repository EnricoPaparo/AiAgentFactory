# Costruisci il tuo Primo Agente

## Obiettivo

Costruiremo un **agente di ricerca e analisi** in Python che:
1. Accetta una domanda dall'utente
2. Cerca informazioni su web e in un database locale
3. Analizza i risultati
4. Genera un report strutturato

Strumenti usati: **Claude API**, **Python**, **Chroma** (vector DB), **Tavily** (ricerca web).

---

## Setup

```bash
pip install anthropic chromadb tavily-python python-dotenv
```

```
# .env
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
```

---

## Step 1: Definisci gli strumenti

```python
# tools.py
import json
import chromadb
from tavily import TavilyClient
import subprocess
import tempfile

chroma_client = chromadb.Client()
knowledge_base = chroma_client.get_or_create_collection("knowledge")
tavily = TavilyClient(api_key="...")

TOOLS = [
    {
        "name": "search_web",
        "description": "Cerca informazioni aggiornate su internet. Usa quando hai bisogno di fatti recenti o notizie.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Query di ricerca"},
                "max_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_knowledge_base",
        "description": "Cerca nella knowledge base locale. Usa per documenti interni e informazioni già indicizzate.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Cosa cercare nella KB"},
                "n_results": {"type": "integer", "default": 3}
            },
            "required": ["query"]
        }
    },
    {
        "name": "run_python",
        "description": "Esegui codice Python per calcoli, analisi dati o trasformazioni. Restituisce stdout.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Codice Python da eseguire"}
            },
            "required": ["code"]
        }
    },
    {
        "name": "save_report",
        "description": "Salva il report finale su file. Usa solo quando hai completato l'analisi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Nome del file (es. report.md)"},
                "content": {"type": "string", "description": "Contenuto del report in Markdown"}
            },
            "required": ["filename", "content"]
        }
    }
]

def handle_tool(name: str, inputs: dict) -> str:
    if name == "search_web":
        results = tavily.search(inputs["query"], max_results=inputs.get("max_results", 5))
        return json.dumps([{"title": r["title"], "url": r["url"], "content": r["content"][:500]} 
                           for r in results.get("results", [])], ensure_ascii=False)
    
    elif name == "search_knowledge_base":
        results = knowledge_base.query(
            query_texts=[inputs["query"]],
            n_results=inputs.get("n_results", 3)
        )
        docs = results.get("documents", [[]])[0]
        return json.dumps(docs, ensure_ascii=False) if docs else "Nessun risultato trovato"
    
    elif name == "run_python":
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(inputs["code"])
            fname = f.name
        result = subprocess.run(["python", fname], capture_output=True, text=True, timeout=30)
        return result.stdout or result.stderr or "(nessun output)"
    
    elif name == "save_report":
        with open(inputs["filename"], "w", encoding="utf-8") as f:
            f.write(inputs["content"])
        return f"Report salvato in {inputs['filename']}"
    
    return "Tool non trovato"
```

---

## Step 2: Il loop dell'agente

```python
# agent.py
import anthropic
from tools import TOOLS, handle_tool

SYSTEM = """Sei un agente di ricerca e analisi esperto.

Quando ricevi una richiesta:
1. Pensa a quali informazioni ti servono
2. Usa search_web per informazioni aggiornate
3. Usa search_knowledge_base per dati interni
4. Usa run_python per calcoli e analisi
5. Sintetizza i risultati
6. Usa save_report per salvare il report finale

Sii metodico, cita le fonti e indica quando non sei sicuro di qualcosa."""

client = anthropic.Anthropic()

def run_agent(task: str, verbose: bool = True) -> str:
    messages = [{"role": "user", "content": task}]
    step = 0
    
    while True:
        step += 1
        if verbose:
            print(f"\n--- Step {step} ---")
        
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages
        )
        
        if verbose:
            for block in response.content:
                if hasattr(block, 'text'):
                    print(f"🤔 {block.text[:200]}{'...' if len(block.text) > 200 else ''}")
                elif block.type == 'tool_use':
                    print(f"🔧 {block.name}({json.dumps(block.input, ensure_ascii=False)[:100]})")
        
        # Fine: l'agente ha la risposta
        if response.stop_reason == "end_turn":
            final = next((b.text for b in response.content if hasattr(b, 'text')), "")
            if verbose:
                print(f"\n✅ Completato in {step} step")
            return final
        
        # Tool use: esegui gli strumenti
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = handle_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            messages.append({"role": "user", "content": tool_results})
        
        # Sicurezza: limite massimo di step
        if step >= 20:
            return "Limite di step raggiunto. Processo interrotto."
```

---

## Step 3: Esecuzione

```python
# main.py
import json
from agent import run_agent

if __name__ == "__main__":
    task = """
    Analizza lo stato attuale dell'AI in Italia nel 2025:
    - Principali aziende e startup nel settore
    - Trend di investimento
    - Regolamentazione (EU AI Act)
    - Opportunità principali
    
    Genera un report completo in Markdown e salvalo come 'report-ai-italia.md'
    """
    
    print("🚀 Avvio agente...\n")
    result = run_agent(task, verbose=True)
    print(f"\n📄 Risposta finale:\n{result}")
```

---

## Output di esempio

```
🚀 Avvio agente...

--- Step 1 ---
🤔 Per analizzare lo stato dell'AI in Italia, cercherò informazioni su...
🔧 search_web({"query": "AI startup Italia 2025 investimenti"})

--- Step 2 ---
🤔 Ho trovato alcune informazioni. Cerco anche dati sulla regolamentazione...
🔧 search_web({"query": "EU AI Act implementazione Italia 2025"})

--- Step 3 ---
🤔 Ora elaboro i dati con Python per identificare trend...
🔧 run_python({"code": "trends = [...]; print(sorted(trends))"})

--- Step 4 ---
🔧 save_report({"filename": "report-ai-italia.md", "content": "# AI in Italia 2025\n..."})

✅ Completato in 4 step

📄 Ho completato l'analisi e salvato il report in 'report-ai-italia.md'
```

---

## Aggiungi memoria persistente

```python
import json
from pathlib import Path

class AgentMemory:
    def __init__(self, path: str = "memory.json"):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}
    
    def save(self, key: str, value):
        self.data[key] = value
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))
    
    def get(self, key: str, default=None):
        return self.data.get(key, default)
    
    def to_context(self) -> str:
        if not self.data:
            return "Nessuna memoria precedente."
        return "Informazioni da sessioni precedenti:\n" + "\n".join(
            f"- {k}: {v}" for k, v in self.data.items()
        )

memory = AgentMemory()

# Aggiungi al system prompt
SYSTEM = f"""Sei un agente esperto...

{memory.to_context()}
"""
```

---

## Checklist per un agente in produzione

- [ ] **Gestione errori**: ogni tool handler ha try/except
- [ ] **Timeout**: i tool non possono girare all'infinito  
- [ ] **Logging**: ogni step viene loggato su file
- [ ] **Limite di step**: ciclo massimo per evitare loop
- [ ] **Validazione input**: i parametri sono controllati prima dell'uso
- [ ] **Rate limiting**: rispetta i limiti API
- [ ] **Secrets**: API key da variabili d'ambiente, mai nel codice
- [ ] **Test**: unit test per ogni tool handler
- [ ] **Human gate**: checkpoint per azioni irreversibili

---

## Prossimi passi

Hai completato AI School! Ecco dove continuare:

- **Anthropic Cookbook** — esempi pratici con Claude API
- **Claude Agent SDK** — framework ufficiale per agenti
- **LangChain / LangGraph** — framework Python per agenti complessi
- **AutoGen (Microsoft)** — multi-agent framework
- **AI Agent Factory** — questo stesso repository con pattern pronti

> Costruire agenti AI è un mix di ingegneria del software e comprensione dei modelli linguistici. La chiave è sperimentare, misurare e iterare.

**Buon building!** ⚡
