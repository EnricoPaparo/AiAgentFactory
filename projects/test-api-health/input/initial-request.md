# Richiesta Iniziale: test-api-health

## Data

2026-06-17

## Richiesta

Sviluppare una REST API minimale in Node.js con le seguenti caratteristiche:

- Endpoint `GET /health` che ritorna HTTP 200 con body JSON:
  ```json
  { "status": "ok", "timestamp": "2026-06-17T10:00:00.000Z" }
  ```
- Porta 3000 configurabile tramite variabile d'ambiente `PORT`
- Test automatico che verifica l'endpoint (Jest, Vitest o similare)
- Dockerfile minimale per containerizzazione

## Vincoli

- Stack: Node.js 20 LTS + Express (o framework HTTP minimale equivalente)
- Nessun database, nessuna autenticazione, nessuna persistenza
- Codice pulito — niente over-engineering
- Il test deve girare con `npm test`
- Il container deve esporsi sulla porta 3000

## Contesto

Progetto di test per validare il flusso end-to-end di AiAgentFactory.

## Criteri di Accettazione

- `GET /health` risponde 200 con JSON valido
- `npm test` passa senza errori
- `docker build` e `docker run -p 3000:3000` funzionano
