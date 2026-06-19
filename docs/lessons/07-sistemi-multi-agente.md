# Sistemi Multi-Agente

## Perché più agenti?

Un singolo agente ha limiti: context window finita, attenzione degradata su task lunghi, difficoltà a parallelizzare lavoro.

I **sistemi multi-agente** superano questi limiti con la specializzazione e la collaborazione:

```
Singolo agente:
  Analizzare + scrivere + revisionare + tradurre = tutto insieme → sovraccarico

Sistema multi-agente:
  Agente Ricercatore → Agente Analista → Agente Scrittore → Agente Revisore
  (parallelo dove possibile, specializzato per task)
```

---

## Pattern fondamentali

### 1. Pipeline sequenziale

Output di un agente = input del successivo.

```
Utente
  ↓
[Agente Scraper] → estrae dati dal web
  ↓
[Agente Analista] → interpreta i dati
  ↓
[Agente Reporter] → genera il report
  ↓
Utente
```

```python
def pipeline(topic: str) -> str:
    raw_data = scraper_agent.run(f"Raccogli dati su: {topic}")
    analysis = analyst_agent.run(f"Analizza questi dati:\n{raw_data}")
    report    = reporter_agent.run(f"Genera un report da questa analisi:\n{analysis}")
    return report
```

### 2. Orchestratore + Subagenti

Un orchestratore centrale coordina agenti specializzati:

```python
ORCHESTRATOR_SYSTEM = """
Sei il coordinatore di un team AI. Il tuo compito è:
1. Analizzare il task ricevuto
2. Decidere quali agenti chiamare e in quale ordine
3. Aggregare i risultati in una risposta coerente

Agenti disponibili:
- research_agent(query): ricerca informazioni sul web
- code_agent(task): scrive ed esegue codice Python
- writing_agent(brief): scrive testi e documenti
- review_agent(content): revisiona e migliora contenuti
"""

def orchestrate(task: str) -> str:
    # L'orchestratore pianifica
    plan = orchestrator.run(f"Pianifica come completare questo task: {task}")
    
    # Esegui il piano
    results = {}
    for step in parse_plan(plan):
        agent = get_agent(step.agent_name)
        results[step.id] = agent.run(step.prompt)
    
    # L'orchestratore aggrega
    return orchestrator.run(f"Sintetizza questi risultati in una risposta:\n{results}")
```

### 3. Agenti paralleli

Più agenti lavorano simultaneamente su subtask indipendenti:

```python
import asyncio

async def parallel_research(topics: list[str]) -> list[str]:
    tasks = [research_agent.arun(topic) for topic in topics]
    results = await asyncio.gather(*tasks)
    return results

# Ricerca su 5 argomenti in parallelo invece che in sequenza
results = asyncio.run(parallel_research([
    "trend AI 2025",
    "startup AI europa",
    "investimenti AI italia",
    "regolamentazione AI UE",
    "open source AI models"
]))
```

### 4. Critic / Evaluator

Un agente speciale valuta l'output degli altri:

```python
def generate_with_critique(task: str, max_iterations: int = 3) -> str:
    content = generator_agent.run(task)
    
    for i in range(max_iterations):
        feedback = critic_agent.run(f"""
Valuta questo output su una scala 1-10 e fornisci feedback specifico:

TASK ORIGINALE: {task}
OUTPUT: {content}

Se il punteggio è >= 8, rispondi con APPROVED.
Altrimenti, specifica cosa migliorare.
""")
        if "APPROVED" in feedback:
            break
        content = generator_agent.run(f"Migliora questo output in base al feedback:\n{feedback}\n\nOutput attuale:\n{content}")
    
    return content
```

---

## Handoff tra agenti

Il **handoff** è il trasferimento controllato di contesto tra agenti:

```python
class Handoff:
    def __init__(self, from_agent: str, to_agent: str, context: dict):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.context = context
        self.timestamp = datetime.now()
    
    def to_prompt(self) -> str:
        return f"""
## Handoff da {self.from_agent}

### Contesto ricevuto:
{json.dumps(self.context, indent=2, ensure_ascii=False)}

### Il tuo compito:
Prendi in carico il lavoro e continua da dove si è fermato {self.from_agent}.
"""
```

Un buon handoff contiene:
- Cosa è stato fatto finora
- Decisioni prese e perché
- Informazioni critiche da non perdere
- Cosa fare esattamente

---

## Supervisore e Human Gates

```python
class Supervisor:
    def __init__(self, agents: dict, human_gate_threshold: float = 0.7):
        self.agents = agents
        self.threshold = human_gate_threshold
    
    def run(self, task: str) -> str:
        # Assegna il task
        assignment = self._assign(task)
        result = self.agents[assignment.agent].run(assignment.prompt)
        
        # Valuta la qualità
        confidence = self._evaluate_confidence(task, result)
        
        # Gate umano se la confidenza è bassa
        if confidence < self.threshold:
            return self._request_human_review(task, result, confidence)
        
        return result
    
    def _request_human_review(self, task, result, confidence):
        print(f"\n⚠️  RICHIESTA REVISIONE UMANA")
        print(f"Confidenza: {confidence:.0%}")
        print(f"Task: {task}")
        print(f"Risultato agente:\n{result}")
        approved = input("\nApprovare? (s/n): ").lower() == 's'
        return result if approved else "Task respinto dall'utente"
```

---

## Memoria condivisa tra agenti

```python
class SharedMemory:
    """Memoria condivisa che tutti gli agenti possono leggere/scrivere"""
    
    def __init__(self):
        self._store = {}
        self._log = []
    
    def write(self, agent: str, key: str, value):
        self._store[key] = value
        self._log.append({"agent": agent, "action": "write", "key": key, "ts": datetime.now().isoformat()})
    
    def read(self, key: str):
        return self._store.get(key)
    
    def get_context(self) -> str:
        """Genera un riassunto leggibile di tutto ciò che è in memoria"""
        return "\n".join([f"- {k}: {v}" for k, v in self._store.items()])

# Uso
memory = SharedMemory()

research_agent.run("Ricerca trend AI", shared_memory=memory)
# → memory.write("research_agent", "ai_trends", ["trend1", "trend2", ...])

analyst_agent.run(
    f"Analizza questi dati:\n{memory.get_context()}", 
    shared_memory=memory
)
```

---

## Anti-pattern nei sistemi multi-agente

### Cascata di errori
Se l'agente 1 sbaglia, l'agente 2 lavora su dati sbagliati. **Soluzione**: validazione tra i passaggi.

### Loop infiniti
Due agenti che si rimandano il task all'infinito. **Soluzione**: limite massimo di iterazioni.

### Contesto perso negli handoff
Informazioni critiche non trasferite. **Soluzione**: schema di handoff standardizzato.

### Over-engineering
Creare sistemi multi-agente per task che un singolo agente può fare. **Soluzione**: inizia semplice, aggiungi complessità solo se necessario.

---

## Quando usare sistemi multi-agente

✅ **Usa multi-agente quando:**
- Il task supera la context window di un singolo agente
- Parti del lavoro possono essere parallelizzate
- Hai bisogno di specializzazione (un esperto per ogni dominio)
- Vuoi review incrociata per aumentare la qualità

❌ **Non usare multi-agente quando:**
- Un singolo agente con buoni tool è sufficiente
- La latenza è critica (ogni handoff aggiunge tempo)
- Non hai bisogno di parallelismo

Nel modulo finale costruiamo un agente reale da zero.
