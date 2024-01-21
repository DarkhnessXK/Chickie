reset_schema:
	poetry run python scripts/reset_schema.py
	poetry run alembic upgrade head

dev:
	poetry run uvicorn asgi:app --reload --host 0.0.0.0 --port 8010
