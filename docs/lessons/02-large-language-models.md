# Come funzionano i Large Language Models

## Cosa sono gli LLM?

Un **Large Language Model (LLM)** è una rete neurale addestrata su enormi quantità di testo per prevedere la parola successiva in una sequenza. Da questa capacità apparentemente semplice emergono comprensione, ragionamento e generazione di testo.

Claude, GPT-4, Gemini, Llama — sono tutti LLM.

---

## Il concetto di Token

Gli LLM non leggono parole, leggono **token**: pezzi di testo che possono essere parole intere, parti di parole o punteggiatura.

```
"Intelligenza artificiale" → ["Intel", "ligen", "za", " artif", "iciale"]
"AI" → ["AI"]
"print('hello')" → ["print", "('", "hello", "')"]
```

**Perché importa?**
- I modelli hanno un limite di token in input+output (**context window**)
- Il costo API si misura in token
- Più token = più lento + più costoso

---

## L'architettura Transformer

Il paper **"Attention is All You Need"** (Google, 2017) ha cambiato tutto.

Il Transformer ha due componenti chiave:

### Self-Attention
Ogni token "guarda" tutti gli altri token e capisce il loro peso relativo per costruire il significato.

```
"La banca del fiume era verde"
"Ho depositato in banca"
```

La parola "banca" ottiene rappresentazioni diverse in base al contesto — questo è il meccanismo di attenzione.

### Feed-Forward Network
Dopo l'attenzione, ogni token passa attraverso una rete neurale che trasforma la sua rappresentazione.

### Stacking
I Transformer impilano decine o centinaia di questi layer. Ogni layer raffina la comprensione.

---

## Pre-training e Fine-tuning

### Pre-training
Il modello viene addestrato su trilioni di token di testo (internet, libri, codice) con un obiettivo semplice:

> *Prevedi il token successivo.*

Questo richiede mesi di calcolo su migliaia di GPU.

### Fine-tuning (RLHF)
Dopo il pre-training, il modello viene raffinato per essere **utile e sicuro**:

1. **SFT** (Supervised Fine-Tuning): esempi di conversazioni umane di alta qualità
2. **RLHF** (Reinforcement Learning from Human Feedback): umani votano le risposte migliori
3. Il modello impara a preferire risposte utili, oneste e innocue

---

## Embeddings

Gli embedding sono **vettori numerici** che rappresentano il significato di un testo nello spazio matematico.

```python
"gatto" → [0.12, -0.87, 0.34, 0.55, ...]  # vettore di 1536 numeri
"felino" → [0.14, -0.82, 0.31, 0.58, ...]  # simile!
"auto"   → [0.91,  0.23, -0.67, 0.02, ...] # distante
```

Testi con significato simile hanno embedding vicini nello spazio vettoriale. Questa proprietà è fondamentale per la ricerca semantica e il RAG (Modulo 6).

---

## Temperature e parametri di generazione

Quando un LLM genera testo, campiona dalla distribuzione di probabilità dei token:

| Parametro | Effetto |
|-----------|---------|
| `temperature: 0` | Deterministico, sempre il token più probabile |
| `temperature: 0.7` | Bilanciato — creativo ma coerente |
| `temperature: 1.5` | Molto creativo, può diventare incoerente |
| `top_p: 0.9` | Considera solo i token che coprono il 90% della probabilità |
| `max_tokens` | Lunghezza massima della risposta |

Per compiti di analisi e ragionamento → `temperature` bassa (0–0.3)  
Per scrittura creativa → `temperature` più alta (0.7–1.0)

---

## I modelli Claude

```
claude-fable-5          ← il più potente (ragionamento avanzato)
claude-opus-4-8         ← bilanciato, ottimo per agenti complessi
claude-sonnet-4-6       ← veloce e capace, ideale per produzione
claude-haiku-4-5        ← leggero e rapido, per task semplici
```

**Come scegliere?**
- Prototipo / test → Haiku (economico e veloce)
- Produzione → Sonnet (ottimo rapporto qualità/costo)
- Task complessi, ragionamento → Opus o Fable

---

## Context Window

La context window è la "memoria di lavoro" del modello: tutto il testo che può processare in una singola chiamata.

```
Sistema: [istruzioni del sistema]
Utente:  [messaggio 1]
AI:      [risposta 1]
Utente:  [messaggio 2]  ← tutto questo deve stare nella context window
AI:      [risposta 2]
```

Modelli moderni hanno context window da 100k a 1M+ token — ma attenzione: più è lunga, più è lenta e costosa.

---

## Limiti degli LLM

- **Hallucination**: inventano fatti con sicurezza
- **Knowledge cutoff**: non sanno cosa è successo dopo la data di addestramento
- **Nessuna memoria persistente**: ogni chiamata ricomincia da zero
- **Non possono agire**: da soli possono solo generare testo

Tutti questi limiti si risolvono **con gli agenti** — argomento del Modulo 4.
