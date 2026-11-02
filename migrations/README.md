# Scripture Studio migrations

This project deliberately uses `scripture_*` tables to avoid changing PhantomVault's trading migrations. For the first deployment, the app creates only its own tables at startup. Before production schema evolution, introduce a separate Alembic/Flask-Migrate history for this service and test against a database backup.

Expected tables:

- scripture_sermons
- scripture_references
- scripture_highlights
- scripture_comments
- scripture_sources
- scripture_matches
