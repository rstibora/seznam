# How to run
`$ docker compose up`

Secrets are commited for convenience (.env and Django secret in settings). Postgres is not mounted to host, so nothing important should be kept in it :)

# Design
I used Django and Postgres as that is the stack you use as I understood it. I am not sure if that is the ideal setup here, maybe it would be simpler to just dump the json into Redis and then reconstruct the objects for the presentation.

I found it surprisingly hard to schedule a regular task for containerized Django.

# Further Work
The app is obviously missing many important things:
- Tests, I think their addition would lead to a bit of refactor, as the code is pretty clumped up.
- Logging is nonexistent.
- Data integrity could be improved (see tasks.py).
- Frontend is not very functional (sorting breaks filtering and vice versa).
- Everything now runs in debug mode.
