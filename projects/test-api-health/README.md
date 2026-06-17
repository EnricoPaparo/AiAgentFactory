# test-api-health

Minimal REST API with a single `GET /health` endpoint that returns JSON status and timestamp.

## Installation

Install dependencies:

```bash
npm ci
```

Or using npm install:

```bash
npm install
```

## Running Locally

Start the server on default port 3000:

```bash
npm start
```

Or use the `node` command directly:

```bash
node src/index.js
```

### Custom Port

Set the `PORT` environment variable to run on a different port:

```bash
PORT=9000 npm start
```

Or:

```bash
PORT=9000 node src/index.js
```

## Testing the Endpoint

Once the server is running, test the `/health` endpoint:

```bash
curl http://localhost:3000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2026-06-17T14:30:45.123Z"
}
```

## Running Tests

Run the Jest test suite:

```bash
npm test
```

The test suite verifies:
- HTTP 200 status code on `GET /health`
- JSON response with `status` and `timestamp` fields
- `status` value is `"ok"`
- `timestamp` is a valid ISO8601 format
- Content-Type is `application/json`

## Docker

### Build

Build the Docker image:

```bash
docker build -t test-api-health .
```

### Run

Run the container and map port 3000:

```bash
docker run -p 3000:3000 test-api-health
```

The API will be available at `http://localhost:3000/health`.

### Custom Port in Docker

To run on a different port, map and set the environment variable:

```bash
docker run -e PORT=8000 -p 8000:8000 test-api-health
```

## Project Structure

```
.
├── src/
│   └── index.js           # Express server and GET /health endpoint
├── __tests__/
│   └── health.test.js     # Jest test suite
├── Dockerfile             # Docker image definition
├── .dockerignore          # Docker build exclusions
├── .gitignore             # Git exclusions
├── package.json           # npm manifest and configuration
└── README.md              # This file
```

## Technology Stack

- **Runtime**: Node.js 20 LTS
- **Framework**: Express.js
- **Testing**: Jest with supertest
- **Containerization**: Docker

## License

MIT
