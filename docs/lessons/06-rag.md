# RAG — Retrieval Augmented Generation

## Il problema che RAG risolve

Gli LLM hanno una knowledge cutoff e non conoscono i tuoi dati privati (documenti aziendali, knowledge base, dati aggiornati).

**RAG** (Retrieval Augmented Generation) risolve questo collegando i tuoi dati agli LLM **senza riaddestrare il modello**.

```
Senza RAG:
  Domanda: "Qual è la policy sulle ferie 2025?"
  LLM: "Non ho informazioni specifiche sulla tua azienda..."

Con RAG:
  1. Recupera la policy dal documento interno
  2. Iniettala nel contesto del prompt
  LLM: "Secondo la policy aziendale 2025, hai diritto a 25 giorni..."
```

---

## Architettura RAG

```
FASE 1 - INDICIZZAZIONE (offline)
─────────────────────────────────
Documenti → Chunking → Embedding → Vector DB

FASE 2 - RETRIEVAL (a runtime)
─────────────────────────────
Query → Embedding → Ricerca vettoriale → Top-K chunks

FASE 3 - GENERAZIONE
────────────────────
[System prompt] + [Chunks recuperati] + [Query] → LLM → Risposta
```

---

## Step 1: Chunking dei documenti

Dividere i documenti in pezzi (chunk) gestibili:

```python
def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Divide il testo in chunk con overlap per non perdere contesto ai bordi"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# Per documenti strutturati (Markdown, PDF), è meglio dividere per sezione
def chunk_by_heading(markdown: str) -> list[dict]:
    import re
    sections = re.split(r'\n#{1,3} ', markdown)
    return [{"content": s, "metadata": {"type": "section"}} for s in sections if s.strip()]
```

**Regola pratica**: chunk da 256-1024 token con overlap del 10-20%.

---

## Step 2: Creare gli Embedding

```python
import anthropic

client = anthropic.Anthropic()

def embed(texts: list[str]) -> list[list[float]]:
    """Genera embedding con il modello di Claude"""
    # Anthropic usa un modello dedicato per gli embedding
    # In alternativa: OpenAI ada-002, Cohere, Sentence Transformers
    response = client.embeddings.create(
        model="voyage-3",  # modello di embedding consigliato da Anthropic
        input=texts
    )
    return [e.embedding for e in response.embeddings]

# Esempio
chunks = ["Python è un linguaggio di programmazione...", "Gli agenti AI..."]
embeddings = embed(chunks)
print(len(embeddings[0]))  # 1024 (dimensione del vettore)
```

---

## Step 3: Vector Database

I vector database permettono ricerca semantica ultra-veloce:

| DB | Caso d'uso | Note |
|----|-----------|------|
| **Chroma** | Sviluppo locale | Facile da usare, in-memory |
| **Pinecone** | Produzione cloud | Managed, scalabile |
| **Weaviate** | Enterprise | Open-source, feature ricche |
| **pgvector** | Già hai PostgreSQL | Estensione Postgres |
| **FAISS** | Alto volume | Libreria Facebook, in-memory |

```python
import chromadb

# Setup
client_db = chromadb.Client()
collection = client_db.create_collection("knowledge_base")

# Indicizza i documenti
collection.add(
    documents=chunks,              # testi originali
    embeddings=embeddings,         # vettori calcolati
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    metadatas=[{"source": "policy.pdf", "page": i} for i in range(len(chunks))]
)

# Ricerca semantica
results = collection.query(
    query_texts=["quanti giorni di ferie ho?"],
    n_results=5  # recupera i 5 chunk più rilevanti
)
print(results["documents"])
```

---

## Step 4: Generazione con contesto recuperato

```python
def rag_query(question: str, collection, client: anthropic.Anthropic) -> str:
    # 1. Recupera i chunk rilevanti
    results = collection.query(query_texts=[question], n_results=4)
    context = "\n\n---\n\n".join(results["documents"][0])
    
    # 2. Costruisci il prompt con il contesto
    system = """Sei un assistente che risponde solo in base ai documenti forniti.
Se la risposta non è nei documenti, dì esplicitamente che non puoi rispondere."""
    
    prompt = f"""Documenti di riferimento:
<context>
{context}
</context>

Domanda: {question}

Rispondi basandoti ESCLUSIVAMENTE sui documenti sopra."""
    
    # 3. Genera la risposta
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# Uso
answer = rag_query("Quanti giorni di ferie spettano a un dipendente junior?", collection, client)
```

---

## Tecniche avanzate di RAG

### Hybrid Search
Combina ricerca semantica (vettoriale) con ricerca lessicale (BM25/TF-IDF):

```python
# Semantica: trova concetti simili
semantic_results = vector_search("ferie dipendenti")

# Lessicale: trova corrispondenze esatte
lexical_results = bm25_search("ferie")

# Combina con Reciprocal Rank Fusion
final_results = rrf_merge(semantic_results, lexical_results)
```

### Re-ranking
Dopo il retrieval iniziale, usa un modello di re-ranking per riordinare per rilevanza:

```python
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Prendi 20 risultati e riordina per trovare i migliori 5
scores = reranker.predict([(question, doc) for doc in top_20_docs])
top_5 = sorted(zip(top_20_docs, scores), key=lambda x: x[1], reverse=True)[:5]
```

### Query Expansion
Genera varianti della query per aumentare il recall:

```python
def expand_query(query: str) -> list[str]:
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"Genera 3 varianti della seguente query per una ricerca semantica. Una per riga:\n{query}"
        }]
    )
    variants = response.content[0].text.strip().split("\n")
    return [query] + variants[:3]
```

---

## Quando usare RAG vs Fine-tuning

| Caratteristica | RAG | Fine-tuning |
|----------------|-----|-------------|
| Dati aggiornabili | ✅ Facilmente | ❌ Richiede nuovo training |
| Costo setup | Basso | Alto (GPU, tempo) |
| Fonti tracciabili | ✅ Sempre | ❌ No |
| Latenza | +50-200ms | Nessun overhead |
| Conoscenza procedurale | Limitata | ✅ Ottima |
| Conoscenza fattuale | ✅ Ottima | ✅ Ottima |

**Regola pratica**: usa RAG per dati che cambiano spesso. Usa fine-tuning per cambiare il *modo* in cui il modello risponde (tono, stile, formato).

---

## Pipeline RAG completa

```python
class RAGPipeline:
    def __init__(self, docs_path: str):
        self.client = anthropic.Anthropic()
        self.db = chromadb.Client()
        self.collection = self.db.create_collection("docs")
        self._index(docs_path)
    
    def _index(self, path: str):
        # Carica, chunka, embedda e indicizza
        documents = load_documents(path)
        for doc in documents:
            chunks = chunk_text(doc.content)
            embeddings = embed(chunks)
            self.collection.add(
                documents=chunks,
                embeddings=embeddings,
                ids=[f"{doc.id}_{i}" for i in range(len(chunks))],
                metadatas=[{"source": doc.name}] * len(chunks)
            )
    
    def query(self, question: str) -> dict:
        results = self.collection.query(query_texts=[question], n_results=5)
        context = "\n\n".join(results["documents"][0])
        sources = list({m["source"] for m in results["metadatas"][0]})
        
        answer = rag_query(question, self.collection, self.client)
        return {"answer": answer, "sources": sources}
```

Nel prossimo modulo vediamo come far collaborare più agenti insieme.
