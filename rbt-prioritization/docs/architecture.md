# Architecture

## Components
- **API Layer (FastAPI)**: request handling, validation (Pydantic), routes for telemetry ingest and priority retrieval.
- **Core (Prioritizer & Explainability)**: risk calculation with transparent weights; per-feature contributions and natural-language explanations.
- **Persistence (SQLite + SQLAlchemy)**: modules, telemetry events, computed risk snapshots.
- **UI (HTMX + Tailwind)**: simple list and drill-down pages.

## Data Model (simplified)
- `Module`: name, owner, domain, last_change_at
- `TelemetryEvent`: module_name, kind, value, at
- `RiskSnapshot`: module_name, score, band, contributions (JSON), created_at

## Flow
1. Ingest telemetry via `/ingest/telemetry` (or use `scripts/load_sample.py`).
2. Compute risk: `/priorities/recompute` or GET `/priorities` (auto computes).
3. Inspect UI: `/` and `/modules/{name}` for explanations + signals.

