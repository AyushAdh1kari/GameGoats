# GameGoats

GameGoats is a multi-persona game-community platform for browsing games, saving favorites, generating recommendations, and managing moderation/admin workflows.

Current repo status:
- Phase 1 setup is in place: branch workflow, Dockerized services, and setup/status pages in Streamlit.
- Phase 2 database foundation is in place: MySQL bootstrap SQL plus synthetic seed data for demos.
- Backend work is in progress: system routes, games routes, and admin/reporting routes are implemented, while the remaining API areas are still being wired.

## Repository Structure

- `app/`: Streamlit frontend
- `api/`: Flask API
- `database-files/`: schema and seed SQL loaded into MySQL on first container creation

## Prerequisites

- Docker Desktop
- Git

Optional local Python setup outside Docker:
- API dependencies: `pip install -r api/requirements.txt`
- Streamlit dependencies: `pip install -r app/src/requirements.txt`

## First-Time Setup

1. Clone the repo.
2. Copy `api/.env.template` to `api/.env`.
3. Replace the placeholder values in `api/.env`:
   - `SECRET_KEY`
   - `MYSQL_ROOT_PASSWORD`
4. Start the full stack:

```bash
docker compose up -d --build
```

## Running Services

After startup, these containers should be available:
- Streamlit app: `http://localhost:8501`
- Flask API: `http://localhost:4000`
- MySQL: `localhost:3200`

## Verify The Stack

### Flask API

- `GET http://localhost:4000/`
- Expected response: service metadata for the GameGoats API

- `GET http://localhost:4000/health`

```json
{"status":"healthy"}
```

- `GET http://localhost:4000/health/db`

```json
{"database":"connected","ping":1}
```

- `GET http://localhost:4000/api/scope`
- Expected response: currently locked resource list for the project

### Streamlit App

- URL: `http://localhost:8501`
- Expected: GameGoats home page plus setup/status pages such as container status, API scope, branching rules, and the Phase 1 checklist

### Database

- The `db` container auto-runs:
  - `database-files/01_gamegoats_bootstrap.sql`
  - `database-files/02_gamegoats_seed_data.sql`
- Schema notes and expected seed counts are documented in `database-files/README.md`

## Current API Surface

Implemented routes currently include:

### System Routes

- `GET /`
- `GET /health`
- `GET /health/db`
- `GET /api/scope`

### Games Routes

- `GET /games`
- `POST /games`
- `GET /games/<game_id>`
- `PUT /games/<game_id>`
- `DELETE /games/<game_id>`

Example `POST /games` request body:

```json
{
  "title": "Skyline Tactics",
  "description": "Squad-based strategy game for CRUD testing.",
  "genre": "Strategy",
  "platform": "PC",
  "release_year": 2026,
  "average_rating": 4.25,
  "lifecycle_status": "active",
  "published_by_studio_id": 1
}
```

### Admin Routes

- `GET /reports`
- `POST /reports`
- `PUT /reports`
- `DELETE /reports`
- `GET /servers`
- `POST /servers`
- `GET /servers/<server_id>`
- `PUT /servers/<server_id>`
- `DELETE /servers/<server_id>`
- `GET /servers/<server_id>/alerts`
- `POST /servers/<server_id>/alerts`
- `PUT /servers/<server_id>/alerts`
- `DELETE /servers/<server_id>/alerts`
- `GET /alert/<alert_id>`
- `PUT /alert/<alert_id>`
- `DELETE /alert/<alert_id>`

Note:
- `games` is now registered in the Flask app and live.
- `users/recommendations` and `studio_developer/community` route files still exist in the repo but are not wired into the Flask app yet.

## Recent Validation

- Live API checks confirmed `GET /games` returns seeded records.
- A full CRUD round trip was verified for the `games` resource:
  - create a game
  - fetch it by id
  - update it
  - delete it
  - confirm the deleted id returns `404`

## Useful Docker Commands

Start the stack:

```bash
docker compose up -d
```

Stop the running containers:

```bash
docker compose stop
```

Remove containers:

```bash
docker compose down
```

Recreate only the database container after schema/seed changes:

```bash
docker compose down db -v
docker compose up -d db
```

## Branch Workflow

- Each teammate should work on their own branch.
- Keep `main` stable.
- Open PRs into `main` instead of pushing directly to it.

## Roles In The Seed Data

The current schema uses these roles:
- `player`
- `recommender`
- `developer`
- `admin`
