# Runtime Adapter: OpenAI Agents SDK

## Scopo

Tradurre un Agent Package generico in un agente eseguibile tramite OpenAI Agents SDK (Python), preservando confini, Human Gate, handoff e Knowledge Candidate definiti nel package.

Questo adapter descrive come mappare i componenti di un Agent Package sul modello di esecuzione dell'OpenAI Agents SDK: `Agent`, `Runner`, `Tool`, `Handoff` e `guardrails`.

## Quando Usarlo

Usare questo adapter quando:

- il progetto usa Python come linguaggio di implementazione;
- si vuole un orchestratore codificato con controllo programmatico del flusso multi-agente;
- il workflow richiede handoff automatici tra agenti con routing condizionale;
- si ha bisogno di tool invocabili dagli agenti (funzioni Python, API, filesystem);
- il team è familiare con l'ecosistema OpenAI.

## Relazione Con Manual Execution

`runtime-adapters/openai-agents-sdk.md` estende `runtime-adapters/manual-execution.md`.

Le regole del Manual Execution Adapter rimangono valide. Questo adapter aggiunge le regole di traduzione specifiche per OpenAI Agents SDK.

In caso di conflitto:

1. Human Gate e boundaries prevalgono sempre, anche su logica di routing automatica;
2. Agent Package prevale sulle preferenze di implementazione SDK;
3. gli standard prevalgono sulle convenzioni SDK quando ci sono ambiguità;
4. runtime hints non possono cambiare scope, strategia o architettura.

## Modello Di Esecuzione

```text
Execution Blueprint
  → un Agent per ogni Agent Package
  → Runner per orchestrare il flusso
  → Tool per ogni capability operativa rilevante
  → Handoff tra agenti come definiti nel package
  → interrupt per Human Gate
```

## Traduzione Agent Package → Agent SDK

### Identità E Istruzioni

```python
from agents import Agent

agent = Agent(
    name="<agent-role>",          # da agent-role nel package
    instructions="""
    <mission del package>

    Responsabilità:
    <responsibilities del package>

    Limiti (non fare):
    <boundaries del package>

    Definition of Done:
    <definition-of-done del package>
    """,
    model="gpt-4o",               # o modello indicato nei runtime-hints
)
```

Le `instructions` devono includere missione, responsabilità, boundaries e Definition of Done dell'Agent Package. Non includere conoscenza tecnica generica — quella va nei tool o come contesto di input.

### Tool

Ogni capability assegnata che richiede un'azione operativa diventa un tool Python:

```python
from agents import function_tool

@function_tool
def leggi_file(percorso: str) -> str:
    """Legge il contenuto di un file nel Project Workspace."""
    with open(percorso) as f:
        return f.read()

@function_tool
def scrivi_file(percorso: str, contenuto: str) -> str:
    """Scrive un file nel Project Workspace."""
    with open(percorso, "w") as f:
        f.write(contenuto)
    return f"File scritto: {percorso}"

@function_tool
def crea_handoff_file(percorso: str, contenuto: str) -> str:
    """Crea il file handoff conforme allo standard."""
    # validare presenza campi obbligatori prima di scrivere
    with open(percorso, "w") as f:
        f.write(contenuto)
    return f"Handoff creato: {percorso}"
```

Regole sui tool:

- ogni tool deve corrispondere a un'azione richiesta dal task o dalle capability assegnate;
- non creare tool per azioni fuori dai boundaries del package;
- i tool non decidono strategia — eseguono operazioni specifiche.

### Handoff Tra Agenti

Gli handoff dell'Agent Package si traducono in oggetti `Handoff` dell'SDK:

```python
from agents import handoff

# handoff da Developer a Reviewer
developer_agent = Agent(
    name="Developer",
    instructions="...",
    handoffs=[handoff(reviewer_agent)]
)
```

L'handoff avviene solo dopo che il Developer ha prodotto il file handoff conforme a `standards/handoff-standard.md`. Il passaggio al Reviewer è condizionato alla presenza del file.

### Esecuzione

```python
from agents import Runner

async def esegui_pipeline():
    result = await Runner.run(
        starting_agent=developer_agent,
        input="Esegui il task dell'Agent Package: " + agent_package_content,
    )
    return result.final_output
```

## Gestione Human Gate

I Human Gate bloccanti si implementano come tool che interrompono l'esecuzione e attendono input umano.

### Approccio Consigliato: Tool Di Controllo Gate

```python
import json
from pathlib import Path
from agents import function_tool

@function_tool
def controlla_human_gate(percorso_gate: str, task_corrente: str) -> str:
    """
    Controlla se un Human Gate blocca il task corrente.
    Restituisce 'approved', 'blocked:<motivo>' o 'not_applicable'.
    """
    gate_content = Path(percorso_gate).read_text()

    # parsing semplificato — adattare al formato reale del gate
    if "status: Pending" in gate_content:
        # verificare se task_corrente è nel blocking-scope
        if task_corrente in gate_content:
            return f"blocked: Human Gate Pending in {percorso_gate}. Attendere decisione umana."
    if "status: Approved" in gate_content:
        return "approved"
    if "status: Rejected" in gate_content:
        return "blocked: Human Gate Rejected. Il workflow non può proseguire."

    return "not_applicable"
```

Il tool di controllo gate deve essere chiamato all'inizio dell'esecuzione e prima di ogni fase critica.

### Flusso Con Human Gate

```python
developer_agent = Agent(
    name="Developer",
    instructions="""
    Prima di iniziare qualsiasi task:
    1. Chiama controlla_human_gate per ogni gate nel Project Workspace.
    2. Se lo stato è 'blocked', fermati e segnala stato blocked nel tuo output.
    3. Se lo stato è 'approved' o 'not_applicable', procedi.
    """,
    tools=[controlla_human_gate, leggi_file, scrivi_file, crea_handoff_file],
)
```

## Gestione Knowledge Candidate

```python
@function_tool
def crea_knowledge_candidate(
    percorso_workspace: str,
    titolo: str,
    descrizione: str,
    destinazione_proposta: str
) -> str:
    """
    Crea una Knowledge Candidate nel Project Workspace.
    Non integra direttamente nella conoscenza permanente.
    """
    import datetime
    contenuto = f"""# Knowledge Candidate: {titolo}

## Metadata

- stato: Proposed
- data-proposta: {datetime.date.today()}
- proposto-da: {agent_role}
- destinazione-proposta: {destinazione_proposta}

## Descrizione

{descrizione}

## Motivazione

[Da completare dall'agente]

## Generalizzabilità

[Da valutare da Knowledge Evolution]
"""
    percorso = f"{percorso_workspace}/knowledge-candidates/{titolo.lower().replace(' ', '-')}.md"
    Path(percorso).write_text(contenuto)
    return f"Knowledge Candidate creata: {percorso}"
```

## Struttura Completa Di Riferimento

```python
# factory_runner.py

from agents import Agent, Runner, handoff, function_tool
from pathlib import Path
import asyncio

# --- Tool di base ---

@function_tool
def leggi_file(percorso: str) -> str:
    """Legge un file del Project Workspace."""
    return Path(percorso).read_text()

@function_tool
def scrivi_file(percorso: str, contenuto: str) -> str:
    """Scrive un file nel Project Workspace."""
    Path(percorso).write_text(contenuto)
    return f"Scritto: {percorso}"

@function_tool
def controlla_human_gate(percorso_gate: str, task_corrente: str) -> str:
    """Controlla se un Human Gate blocca il task corrente."""
    content = Path(percorso_gate).read_text()
    if "status: Pending" in content and task_corrente in content:
        return f"blocked: gate Pending in {percorso_gate}"
    if "status: Approved" in content:
        return "approved"
    if "status: Rejected" in content:
        return "blocked: gate Rejected"
    return "not_applicable"

# --- Agenti ---

reviewer_agent = Agent(
    name="Reviewer",
    instructions="""
    Sei il Reviewer dell'Agent Package <reviewer-package-id>.
    [missione, responsabilità, boundaries, DoD dal package]
    """,
    tools=[leggi_file, scrivi_file],
)

developer_agent = Agent(
    name="Developer",
    instructions="""
    Sei il Developer dell'Agent Package <developer-package-id>.
    Prima di iniziare: chiama controlla_human_gate per ogni gate nel workspace.
    [missione, responsabilità, boundaries, DoD dal package]
    """,
    tools=[controlla_human_gate, leggi_file, scrivi_file],
    handoffs=[handoff(reviewer_agent)],
)

# --- Esecuzione ---

async def main():
    agent_package = Path("projects/<id>/generated-agents/<package>.md").read_text()
    result = await Runner.run(
        starting_agent=developer_agent,
        input=f"Esegui l'Agent Package:\n\n{agent_package}",
    )
    print(result.final_output)

asyncio.run(main())
```

## Limiti Di Questo Adapter

- L'OpenAI Agents SDK non ha un meccanismo nativo di pausa sincrona per Human Gate. Il tool `controlla_human_gate` è una soluzione procedurale — per gate con vera attesa umana, considerare `runtime-adapters/github-actions.md` o un loop esterno con polling.
- Il routing tra agenti via `Handoff` è automatico — assicurarsi che le istruzioni di ogni agente includano i boundaries correttamente per evitare escalation non previste.
- La finestra di contesto del modello può essere un vincolo su Agent Package molto grandi — usare tool per caricare contenuto su richiesta invece di iniettarlo tutto nelle istruzioni.

## Failure Mode Da Evitare

- Inserire tutta la conoscenza tecnica nelle `instructions` invece di usare tool o input contestuali.
- Usare un solo agente per eseguire più Agent Package nello stesso `Runner.run()` senza handoff formali.
- Saltare il controllo Human Gate perché il routing SDK è automatico.
- Modificare conoscenza permanente (archetype, capability, standard) da un tool dell'agente.
- Creare Knowledge Candidate e poi integrarla direttamente senza Knowledge Evolution.
- Confondere `Handoff` SDK (passaggio di esecuzione) con `handoff` AgentFactory (file contratto).

## Criteri Di Completamento Dell'Adapter

Questo adapter è applicato correttamente quando:

1. ogni Agent Package è tradotto in un singolo `Agent` con instructions da missione, responsabilità, boundaries e DoD;
2. le capability assegnate sono implementate come tool specifici;
3. i Human Gate sono controllati tramite tool prima dell'esecuzione;
4. gli handoff tra agenti producono file conformi a `standards/handoff-standard.md`;
5. le Knowledge Candidate sono create nel Project Workspace, non integrate direttamente;
6. lo stato finale è dichiarato e tracciabile.
