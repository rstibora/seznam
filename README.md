# How to run
`$ docker compose up`

Secrets are commited for convenience (.env and Django secret in settings). Postgres is not mounted to host, so nothing important should be kept in it :)

Django rendered frontend runs on port 8000, Svelte that consumes DRF API on port 3000.
