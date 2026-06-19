# Prompt Engineering

## Cos'è il Prompt Engineering?

Il **Prompt Engineering** è l'arte di scrivere istruzioni efficaci per ottenere il meglio da un LLM. Un buon prompt può fare la differenza tra una risposta inutile e una risposta straordinaria.

> I modelli non leggono le tue intenzioni — leggono le tue parole.

---

## I principi fondamentali

### 1. Sii specifico e diretto

❌ Cattivo:
```
Scrivi qualcosa sul marketing.
```

✅ Buono:
```
Scrivi 3 idee per post LinkedIn su come le PMI italiane 
possono usare l'AI per ridurre i costi operativi. 
Tono professionale ma accessibile, max 150 parole ciascuno.
```

### 2. Fornisci contesto
Il modello non conosce il tuo progetto, il tuo team, i tuoi obiettivi. Diglielo.

### 3. Specifica il formato di output

```
Rispondi in formato JSON con i campi: "titolo", "descrizione", "priorità" (alta/media/bassa).
```

### 4. Definisci il ruolo

```
Sei un esperto di cybersecurity con 15 anni di esperienza in aziende fintech. 
Analizza questo codice cercando vulnerabilità.
```

---

## Tecniche avanzate

### Zero-shot
Il modello risponde senza esempi:
```
Classifica questo testo come positivo, negativo o neutro:
"Il servizio era lento ma il cibo eccellente."
```

### Few-shot
Fornisci 2-5 esempi per guidare il comportamento:
```
Classifica il sentiment:
"Ottimo prodotto!" → positivo
"Pessima esperienza" → negativo
"Il pacco è arrivato" → neutro

Ora classifica: "Non mi aspettavo così tanta qualità per questo prezzo!"
```

### Chain-of-Thought (CoT)
Chiedi al modello di ragionare passo dopo passo:

```
Risolvi questo problema pensando ad alta voce, passo dopo passo:
Un'azienda ha 240 dipendenti. Il 30% lavora in remoto. 
Di quelli in remoto, il 25% è part-time. Quanti sono part-time in remoto?
```

Il CoT migliora drasticamente le performance su compiti matematici e logici.

### Self-Consistency
Genera la stessa risposta più volte e prendi la più frequente. Utile per ragionamento complesso.

---

## System Prompt

Il **system prompt** definisce il comportamento globale dell'assistente:

```python
system = """
Sei un assistente per il supporto tecnico di SoftwareCo.
- Rispondi sempre in italiano
- Se non sei sicuro, dì esplicitamente che non lo sai
- Per problemi di fatturazione rimanda sempre all'email billing@softwareco.it
- Non discutere di prodotti concorrenti
- Stile: professionale ma cordiale
"""
```

Il system prompt è il tuo "carattere permanente" — rimane uguale per tutta la conversazione.

---

## Prompt per struttura dell'output

```
Analizza questo business plan e rispondi con ESATTAMENTE questa struttura:

## Punti di forza
- [elenco puntato]

## Rischi principali
- [elenco puntato]

## Raccomandazione
[1 paragrafo]

## Punteggio
[numero da 1 a 10 con breve motivazione]
```

---

## Tecniche per ridurre le hallucination

### Chiedi le fonti
```
Rispondi solo con informazioni che puoi verificare. 
Se non sei certo di qualcosa, scrivi esplicitamente "Non ho certezza su questo punto."
```

### Grounding con contesto
```
Basandoti SOLO sul seguente documento, rispondi alla domanda:

[DOCUMENTO]
...testo del documento...
[/DOCUMENTO]

Domanda: ...
```

### Verifica interna
```
Prima di rispondere, verifica che la tua risposta sia logicamente coerente 
e non contenga contraddizioni. Se ne trovi, correggile.
```

---

## Prompt per agenti

Quando costruisci agenti, il prompt diventa ancora più critico:

```
Sei un agente AI specializzato nell'analisi di contratti legali.

## Obiettivo
Analizzare contratti e identificare clausole rischiose per il cliente.

## Strumenti disponibili
- search_clauses(query): cerca clausole specifiche nel documento
- flag_risk(clause, severity, reason): segnala una clausola rischiosa
- generate_summary(): genera il report finale

## Processo
1. Leggi il contratto completo
2. Identifica e analizza ogni clausola importante
3. Flagga le clausole rischiose con severity: alta/media/bassa
4. Genera il summary finale

## Vincoli
- Non dare mai consigli legali definitivi
- Indica sempre che il parere di un avvocato è necessario
- Sii preciso sui numeri e sulle date citati
```

---

## Anti-pattern comuni

| Errore | Problema | Soluzione |
|--------|----------|-----------|
| Prompt ambiguo | Output imprevisto | Sii specifico |
| Nessun esempio | Il modello "indovina" il formato | Aggiungi few-shot |
| Troppo lungo | Il modello "dimentica" le istruzioni iniziali | Metti le istruzioni chiave all'inizio E alla fine |
| "Scrivi il meglio possibile" | Soggettivo, inutile | Definisci criteri concreti |
| No formato output | Devi fare parsing manuale | Specifica JSON/Markdown/elenco |

---

## Template universale

```
[RUOLO]: Sei un esperto di...
[CONTESTO]: Stiamo lavorando su...
[OBIETTIVO]: Il tuo compito è...
[INPUT]: {variabile}
[VINCOLI]: Non fare X, fai sempre Y
[OUTPUT]: Rispondi con questo formato...
[ESEMPIO]: Per esempio...
```

Nella prossima lezione entriamo nel cuore del corso: gli **Agenti AI**.
