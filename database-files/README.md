# Database Files

The SQL files in this folder execute automatically when the `db` container is created.

## Execution Order

1. `01_gamegoats_bootstrap.sql`
   - creates `gamegoats_db`
   - creates schema tables and foreign keys for:
     - `users`
     - `games`
     - `comments`
     - `favorites`
     - `recommendations`
     - `reports`
     - `servers`
     - `alerts`
2. `02_gamegoats_seed_data.sql`
   - inserts synthetic data for all tables

## Expected Seed Volumes

- Strong entities:
  - `users`: 36
  - `games`: 35
  - `servers`: 30
- Weak entities:
  - `comments`: 60
  - `recommendations`: 60
  - `reports`: 55
  - `alerts`: 55
- Bridge/entity-resolution table:
  - `favorites`: 140

## Recreate Database Container

Use this after changing schema or seed data:

```bash
docker compose down db -v
docker compose up -d db
```

## Manual CRUD Validation (Phase 2)

Example transaction-based checks (safe, rolls back at the end):

```bash
docker compose exec db mysql -uroot -p<MYSQL_ROOT_PASSWORD> -D gamegoats_db -e "
START TRANSACTION;
INSERT INTO games (title, genre, platform, release_year, average_rating, lifecycle_status)
VALUES ('Phase2 Txn Validation', 'Strategy', 'PC', 2026, 4.25, 'active');
UPDATE reports
SET report_status='resolved', assigned_moderator_id=29, resolution_notes='Transactional validation only.'
WHERE report_id=1;
DELETE FROM favorites WHERE favorite_id=1;
ROLLBACK;
"
```
