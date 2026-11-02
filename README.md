# PhantomVault Scripture Studio

A standalone Flask, Jinja, SQLAlchemy, PostgreSQL, Flask-Login, and Flask-WTF workspace built in the PhantomVault design language. It reuses the existing PhantomVault `users` table for login and keeps its own tables prefixed with `scripture_`, so it can share the same PostgreSQL database without altering the trading app.

## Included in this prototype

- Shared PhantomVault email/password verification
- Private sermon notebook with create, edit, delete, search, and filters
- Sermon metadata: title, date, speaker, location/event, topic, notes
- Manual Scripture references with translation/source identifiers
- Text highlight records with colors and anchors
- Comments attached to highlights
- Manual Scripture match records clearly labeled exact, partial, related, or unverified
- Rights-safe behavior: no Bible text is bundled, scraped, generated, or claimed as verified
- Render deployment files and health endpoint
- Persistent English/Runyankore interface toggle in the sidebar

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

A local SQLite database is used unless `DATABASE_URL` is set. For production, set the same PostgreSQL `DATABASE_URL` used by PhantomVault, ideally with a restricted database role. The app creates only its six `scripture_*` tables; it does not create or modify the `users` table.

## Runyankore interface toggle

Signed-in users can press the `Runyankore` button in the sidebar to switch the interface language. The selection is saved in browser local storage and can be switched back with the `English` button. The initial translation covers the application chrome, navigation, forms, and safety labels. Sermon titles, notes, references, highlights, and comments remain unchanged because they are user-authored content. The Runyankore interface copy should be reviewed by a native speaker before treating it as a final published translation.

## Render

Create a separate Render Web Service from this repository and set `DATABASE_URL` to the existing PostgreSQL database connection string. Add a separate `SECRET_KEY`; sessions are separate from PhantomVault even though credentials are shared. Set `APP_BASE_URL` to the Scripture Studio URL. Keep `BIBLE_PROVIDER` as `not-configured` until translation rights and an authorised provider are confirmed.

## Important rights boundary

NKJV, Luganda, and Runyankore/Baibuli Erikwera editions may have different copyright and API terms. This first package stores references and user-authored notes only. Do not add full text, phrase search, semantic matching, audio, AI processing, or exports until the exact edition, provider, license, retention, and permitted uses are confirmed.
