#!/bin/sh

# Apply database migrations
alembic upgrade head

# Start Uvicorn server
exec "$@"
