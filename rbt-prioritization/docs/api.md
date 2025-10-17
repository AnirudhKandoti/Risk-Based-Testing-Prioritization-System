# API

### POST /ingest/telemetry
Body:
```json
{
  "module_name": "checkout",
  "events": [
    {"kind": "error_rate", "value": 0.08, "at": "2025-10-15T12:00:00Z"},
    {"kind": "change_frequency", "value": 7, "at": "2025-10-15T12:00:00Z"}
  ]
}
```

### GET /priorities
Query:
- `limit` (default 50)
- `recompute` (bool, default true)

### POST /priorities/recompute
Forces recomputation from latest telemetry snapshot.

### GET /modules/{name}
Returns module details, latest risk, and explanation.
