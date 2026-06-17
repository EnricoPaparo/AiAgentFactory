# Runtime Adapter: LangGraph

## Scopo

Tradurre un Agent Package e un Execution Blueprint in un grafo LangGraph eseguibile, preservando confini, Human Gate, handoff e Knowledge Candidate definiti nel package.

Questo adapter descrive come mappare la struttura AgentFactory sul modello a grafo di LangGraph: nodi (agenti), archi (handoff/routing), stato condiviso, interrupt per Human Gate e checkpointing per persistenza.

## Quando Usarlo

Usare questo adapter quando:

- il team usa Python e il framework LangChain/LangGraph;
- il workflow ha routing condizionale tra agenti basato su output intermedi;
- si vuole persistenza dello stato tra esecuzioni (checkpoint);
- il progetto richiede human-in-the-loop con vera sospensione del grafo;
- si vuole visualizzazione del grafo di esecuzione per debugging e monitoring.

## Relazione Con Manual Execution

`runtime-adapters/langgraph.md` estende `runtime-adapters/manual-execution.md`.

Le regole del Manual Execution Adapter rimangono valide. Questo adapter aggiunge le regole di traduzione specifiche per LangGraph.

In caso di conflitto:

1. Human Gate e boundaries prevalgono sempre, anche sul routing automatico del grafo;
2. Agent Package prevale sulle preferenze di implementazione LangGraph;
3. gli standard prevalgono sulle convenzioni LangGraph quando ci sono ambiguità.

## Modello Di Esecuzione

```text
Execution Blueprint
  → StateGraph con uno stato condiviso del progetto
  → un nodo per ogni Agent Package
  → archi tra nodi come definiti nel workflow dell'Execution Blueprint
  → interrupt() per Human Gate bloccanti
  → checkpointer per persistenza tra sessioni
```

## Traduzione Execution Blueprint → Grafo

### Stato Condiviso Del Progetto

Lo stato del grafo trasporta il contesto del progetto tra i nodi:

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator

class FactoryState(TypedDict):
    project_id: str
    messages: Annotated[list, operator.add]    # storico messaggi agenti
    current_agent: str                          # agente attivo
    handoffs: dict[str, str]                    # percorsi file handoff prodotti
    human_gates: dict[str, str]                 # stato Human Gate (gate-id → status)
    deliverables: list[str]                     # percorsi deliverable prodotti
    knowledge_candidates: list[str]             # percorsi Knowledge Candidate
    final_status: str                           # completed / blocked / failed
    error: str | None                           # messaggio errore se presente
```

### Nodo Per Agent Package

Ogni Agent Package diventa un nodo nel grafo:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pathlib import Path

def crea_nodo_agente(package_path: str, workspace_path: str):
    """
    Crea un nodo LangGraph da un Agent Package AgentFactory.
    """
    package_content = Path(package_path).read_text()
    llm = ChatOpenAI(model="gpt-4o")

    def nodo(state: FactoryState) -> dict:
        # 1. Controllo Human Gate
        for gate_id, gate_status in state["human_gates"].items():
            if gate_status == "Pending":
                return {
                    "final_status": "blocked",
                    "error": f"Human Gate '{gate_id}' è Pending. Attendere approvazione umana."
                }

        # 2. Preparazione contesto
        system_prompt = f"""
Sei un agente temporaneo AgentFactory in esecuzione tramite LangGraph Runtime Adapter.

Adapter attivi:
- runtime-adapters/langgraph.md
- runtime-adapters/manual-execution.md

Agent Package:
{package_content}

Regole operative:
- Esegui solo il task assegnato nel package.
- Rispetta boundaries, responsibilities e Definition of Done.
- Non modificare standard permanenti, archetype, capability o agenti permanenti.
- Produci solo gli output richiesti.
- Al termine riepiloga: stato finale, file creati, verifiche eseguite, rischi residui.
"""

        # 3. Caricamento input dal workspace
        inputs_content = []
        for input_ref in ["blueprints/", "generated-agents/"]:
            input_path = Path(workspace_path) / input_ref
            if input_path.exists():
                for f in input_path.glob("*.md"):
                    inputs_content.append(f"=== {f} ===\n{f.read_text()}")

        user_message = "Esegui il task dell'Agent Package.\n\nInput disponibili:\n" + "\n\n".join(inputs_content)

        # 4. Esecuzione
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ])

        # 5. Scrittura handoff (il modello produce il contenuto, il nodo lo scrive)
        # In implementazione reale: parsare l'output del modello per estrarre handoff
        return {
            "messages": [response],
            "current_agent": package_path,
            "final_status": "completed"
        }

    return nodo
```

### Costruzione Del Grafo

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

def costruisci_grafo(project_id: str) -> StateGraph:
    workspace = f"projects/{project_id}"

    # Creare i nodi da Agent Package
    developer_node = crea_nodo_agente(
        f"{workspace}/generated-agents/developer.md",
        workspace
    )
    reviewer_node = crea_nodo_agente(
        f"{workspace}/generated-agents/reviewer.md",
        workspace
    )
    supervisor_node = crea_nodo_agente(
        "agents/pipeline-supervisor/pipeline-supervisor.md",
        workspace
    )

    # Costruire il grafo
    builder = StateGraph(FactoryState)

    builder.add_node("developer", developer_node)
    builder.add_node("reviewer", reviewer_node)
    builder.add_node("pipeline_supervisor", supervisor_node)

    # Archi — traducono il workflow dell'Execution Blueprint
    builder.set_entry_point("developer")
    builder.add_edge("developer", "reviewer")
    builder.add_edge("reviewer", "pipeline_supervisor")
    builder.add_edge("pipeline_supervisor", END)

    # Checkpointer per persistenza
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)
```

## Gestione Human Gate Con Interrupt

LangGraph supporta interruzioni native del grafo tramite `interrupt()`. Questo è il meccanismo corretto per implementare Human Gate bloccanti.

### Approccio Con interrupt()

```python
from langgraph.types import interrupt

def nodo_con_human_gate(state: FactoryState) -> dict:
    """
    Nodo che si ferma prima dell'azione critica e attende approvazione umana.
    """
    # Eseguire il task preliminare
    output_preliminare = esegui_task_preliminare(state)

    # Punto di interruzione — il grafo si sospende qui
    decisione = interrupt({
        "tipo": "human_gate",
        "descrizione": "Approvare il deliverable prima di procedere?",
        "output_prodotto": output_preliminare,
        "blocking_scope": "tutto il workflow downstream",
        "istruzioni": "Rispondere con 'approved' o 'rejected: <motivo>'."
    })

    # Riprendere dopo la decisione umana
    if decisione.startswith("rejected"):
        motivo = decisione.replace("rejected:", "").strip()
        return {
            "final_status": "blocked",
            "error": f"Human Gate rifiutato: {motivo}"
        }

    # Aggiornare il file Human Gate nel workspace
    aggiorna_file_human_gate(state["project_id"], "approved")

    return {"final_status": "approved", **output_preliminare}
```

### Esecuzione Con Interrupt

```python
import asyncio
from langgraph.types import Command

async def esegui_con_human_gate(grafo, state_iniziale, thread_id):
    config = {"configurable": {"thread_id": thread_id}}

    # Prima esecuzione — si ferma all'interrupt
    async for event in grafo.astream(state_iniziale, config):
        print(event)

    # A questo punto il grafo è sospeso — attendere input umano
    print("\nGrafo sospeso per Human Gate. Attendere approvazione umana.")
    print("Snapshot corrente:", grafo.get_state(config))

    # Simulare approvazione umana (in produzione: UI, API, o input CLI)
    decisione_umana = input("Approvare? (approved/rejected: motivo): ")

    # Riprendere il grafo con la decisione
    async for event in grafo.astream(Command(resume=decisione_umana), config):
        print(event)
```

### Comportamento Per Stato Human Gate

| Stato | Comportamento LangGraph |
|---|---|
| `Pending` | `interrupt()` sospende il grafo |
| `Approved` | `Command(resume=...)` riprende il grafo |
| `Rejected` | Nodo termina con `final_status: blocked` |
| `Changes Requested` | Nodo ritorna al nodo indicato in `return-to-phase` |
| `Expired` | Trattare come `Rejected` con motivo specifico |

## Routing Condizionale

Tradurre review gate con esito variabile in archi condizionali:

```python
def router_dopo_review(state: FactoryState) -> str:
    """
    Routing condizionale basato sull'esito della review.
    """
    last_message = state["messages"][-1].content

    if "approved" in last_message.lower():
        return "pipeline_supervisor"
    elif "changes_requested" in last_message.lower():
        return "developer"          # torna al Developer per correzioni
    else:
        return END                  # fallimento — terminare

builder.add_conditional_edges(
    "reviewer",
    router_dopo_review,
    {
        "pipeline_supervisor": "pipeline_supervisor",
        "developer": "developer",
        END: END
    }
)
```

## Persistenza E Checkpointing

Usare il checkpointer per persistere lo stato tra sessioni — utile per progetti multi-giorno:

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Persistenza su file SQLite (per sviluppo/test)
with SqliteSaver.from_conn_string("factory_state.db") as checkpointer:
    grafo = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "project-my-project-run-1"}}

    # Prima esecuzione
    result = grafo.invoke(state_iniziale, config)

    # Riesecuzione dallo stesso punto (es. dopo Human Gate risolto)
    result = grafo.invoke(None, config)   # None = riprendere dallo stato salvato
```

## Gestione Knowledge Candidate

```python
from pathlib import Path
import datetime

def crea_knowledge_candidate_da_nodo(
    state: FactoryState,
    titolo: str,
    descrizione: str,
    destinazione: str
) -> dict:
    """
    Crea una Knowledge Candidate nel Project Workspace dal nodo corrente.
    Non integra nella conoscenza permanente.
    """
    contenuto = f"""# Knowledge Candidate: {titolo}

## Metadata

- stato: Proposed
- data-proposta: {datetime.date.today()}
- progetto: {state['project_id']}
- destinazione-proposta: {destinazione}

## Descrizione

{descrizione}
"""
    slug = titolo.lower().replace(" ", "-")
    percorso = f"projects/{state['project_id']}/knowledge-candidates/{slug}.md"
    Path(percorso).write_text(contenuto)

    return {
        "knowledge_candidates": [percorso]
    }
```

## Visualizzazione Del Grafo

LangGraph permette di visualizzare il grafo — utile per validare che l'Execution Blueprint sia stato tradotto correttamente:

```python
# Visualizzazione come Mermaid
print(grafo.get_graph().draw_mermaid())

# Salvataggio come PNG (richiede dipendenze grafiche)
grafo.get_graph().draw_mermaid_png(output_file_path="workflow.png")
```

Il grafo visualizzato deve corrispondere al workflow definito nell'Execution Blueprint.

## Limiti Di Questo Adapter

- LangGraph gestisce lo stato in memoria o su database — per progetti con molti file, preferire artifact file-based (come in `runtime-adapters/github-actions.md`) rispetto allo stato del grafo.
- Il routing condizionale richiede che l'output del modello sia parsabile — definire formati di output chiari nelle istruzioni di ogni nodo.
- L'interrupt LangGraph non è thread-safe in tutte le implementazioni di checkpointer — verificare la compatibilità prima dell'uso in produzione.
- La finestra di contesto può essere un vincolo su grafi con molti nodi e stato accumulato — usare `trim_messages` o stati distinti per nodo.

## Failure Mode Da Evitare

- Mettere tutto il contesto del progetto nello stato del grafo — usare file e percorsi nello stato, non contenuto completo.
- Usare archi diretti per tutti i casi senza routing condizionale — i review gate richiedono routing basato su esito.
- Non implementare `interrupt()` per Human Gate — usare variabili di stato non è sufficiente, il grafo proseguirebbe automaticamente.
- Modificare conoscenza permanente da un nodo del grafo — solo Knowledge Candidate nel Project Workspace.
- Usare un thread_id unico per progetti diversi — ogni progetto deve avere thread_id distinto per garantire isolamento dello stato.
- Creare Knowledge Candidate e poi integrarla direttamente senza Knowledge Evolution.

## Criteri Di Completamento Dell'Adapter

Questo adapter è applicato correttamente quando:

1. ogni Agent Package corrisponde a un nodo distinto nel grafo;
2. gli archi tra nodi riproducono il workflow dell'Execution Blueprint;
3. i Human Gate sono implementati tramite `interrupt()` con vera sospensione del grafo;
4. il checkpointer è configurato per persistenza tra sessioni;
5. i routing condizionali dei review gate hanno archi espliciti per ogni caso (approved, changes_requested, failed);
6. le Knowledge Candidate sono scritte nel Project Workspace, non integrate direttamente;
7. lo stato finale è dichiarato e tracciabile nel campo `final_status`.
