SHELL := /bin/bash

.PHONY: init run test lint format load-sample api-docs

init:
	python -m app.database --init

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest -q

lint:
	ruff check .

format:
	ruff check . --fix
	black .

load-sample:
	python scripts/load_sample.py

api-docs:
	python - <<'PY'\
import json, requests; print("Open http://127.0.0.1:8000/docs")\
PY
