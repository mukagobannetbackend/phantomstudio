# Deployment and shared-account integration

Create this as a separate Render Web Service. Set `DATABASE_URL` to the same PostgreSQL database used by PhantomVault. The application maps the existing `users` table only to verify credentials and creates six independent `scripture_*` tables. It does not call `db.create_all()` for the user table and does not modify PhantomVault migrations.

For safer production access, create a restricted PostgreSQL role that can SELECT from `users` and create/read/write only the `scripture_*` tables. Run against a backup or staging database first. Set a different `SECRET_KEY` from PhantomVault because sessions are intentionally separate.

The first release is reference-first. Add a Bible provider only after confirming the exact NKJV, Luganda, or Runyankore edition, license, API terms, retention rules, and whether phrase search or AI processing is allowed. Keep provider credentials in Render environment variables.
