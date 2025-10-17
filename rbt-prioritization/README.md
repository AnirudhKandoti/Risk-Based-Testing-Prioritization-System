# Risk-Based Testing Prioritization System

A production-ready reference implementation for **Risk-Based Testing (RBT)** that:
- Ingests system telemetry and code change signals.
- Prioritizes modules for regression and monitoring based on a configurable risk model.
- Provides **explainable** (XAI-style) per-module context and **feature-level contributions** for every prioritization decision.
- Ships with an API (FastAPI), minimal web UI (HTMX + Tailwind), CLI utilities, SQLite storage, tests, and CI.

## Quick Start

### 1) Python environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Initialize DB and load sample data
```bash
make init
make load-sample
```

### 3) Run the server
```bash
make run
# Open http://127.0.0.1:8000
```

### 4) Run tests
```bash
make test
```

### 5) Docker
```bash
docker build -t rbt-system .
docker run -p 8000:8000 rbt-system
```

## Why this project?

Risk-Based Testing helps teams focus limited test and monitoring capacity on the most critical, failure-prone, and user-impacting areas. This repo demonstrates:
- A transparent risk-scoring function with **configurable weights** (no black box).
- Lightweight **anomaly signals** built from telemetry time windows.
- **Explanations** with feature contributions and natural-language rationales you can paste into test plans or incident reviews.
- A tiny UI to inspect priorities and drill down.

## Architecture

- **FastAPI** service exposes:
  - `/ingest/telemetry` to POST telemetry events
  - `/priorities` to compute & fetch prioritized modules
  - `/modules/{name}` to view module details + XAI explanation
- **SQLite + SQLAlchemy** for persistence
- **Prioritizer** computes risk from normalized features (error rate, recent change, churn, complexity, SLA breaches, customer impact, test flakiness).
- **Explainability** returns per-feature contributions & reasons.
- **HTMX** pages for quick exploration (no JS framework required).

See `/docs/architecture.md` and `/docs/risk_model.md` for more details.
