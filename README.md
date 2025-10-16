# Doctor Verification API

Backend service for verifying Indian doctors using the scraped NMC database.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# update .env
psql $DATABASE_URL -f migrations/001_init.sql
uvicorn main:app --reload
```

The app will default to a local SQLite database (`./app.db`) if `DATABASE_URL` is not set. On startup it auto-creates tables and seeds a couple of dummy doctors so you can test immediately.

If you prefer Postgres, set `DATABASE_URL` accordingly and run the migration above.