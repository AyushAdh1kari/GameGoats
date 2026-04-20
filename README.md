# GameGoats

Phase 1 setup baseline for CS 3200.

## Project Overview

GameGoats is a multi-persona platform for managing game-community activity and safety signals.

Phase 1 focuses on team setup only:
- clean template leftovers,
- lock route/resource scope in a REST matrix,
- define branching workflow,
- confirm Docker startup for API, database, and Streamlit.

No schema build or full feature implementation is included yet.

## Repository Structure

- `app/`: Streamlit frontend
- `api/`: Flask API
- `database-files/`: SQL files executed when MySQL container is created
- `docs/`: project planning artifacts (REST matrix, branching rules)

## Phase 1 Docs

- REST API matrix: `docs/rest-api-matrix.md`
- Branching strategy: `docs/branching-strategy.md`

## Prerequisites

- Docker Desktop (running)
- Git

Optional for local linting/editor support (outside Docker):
- Python 3.11+
- Install project dependencies with:

```bash
pip install -r requirements.txt
```

## First-Time Setup

1. Clone the repo.
2. Create `api/.env` from `api/.env.template`.
3. Replace placeholder values in `api/.env`:
   - `SECRET_KEY`
   - `MYSQL_ROOT_PASSWORD`
4. Start all containers:

```bash
docker compose up -d --build
```

## Verify Services

### 1) Flask API

- URL: `http://localhost:4000/health`
- Expected JSON:

```json
{"status":"healthy"}
```

### 2) Database (through API health route)

- URL: `http://localhost:4000/health/db`
- Expected JSON:

```json
{"database":"connected","ping":1}
```

### 3) Streamlit App

- URL: `http://localhost:8501`
- Expected: GameGoats home page with navigation buttons for setup pages.

## Useful Docker Commands

Start stack:

```bash
docker compose up -d
```

Stop stack:

```bash
docker compose stop
```

Remove containers:

```bash
docker compose down
```

Recreate database container (after SQL changes):

```bash
docker compose down db -v
docker compose up db -d
```

## Branch Workflow

- Work on your own branch.
- Open PRs into `main`; do not push directly to `main`.
