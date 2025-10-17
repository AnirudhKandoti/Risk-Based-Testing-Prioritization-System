# Risk Model

We compute a **risk score** in `[0, 100]`:

```
score = 100 * sum( w_i * norm_i(value_i) ) / sum(w_i)
```

Where features (example defaults) are:
- `error_rate` (w=5) – fraction of failing requests/tests
- `change_frequency` (w=4) – commits or deployments in recent window
- `code_churn` (w=3) – lines added/removed recently
- `complexity` (w=2) – static analysis index (0..1 normalized)
- `customer_impact` (w=4) – proxy for #active users/ARR
- `sla_breaches` (w=3) – count in recent window
- `test_flakiness` (w=2) – fraction of flaky tests

**Explainability**: we return per-feature contributions
`contrib_i = 100 * w_i * norm_i(value_i) / sum(w_i)` plus textual reasons
based on thresholds (e.g., "error_rate above 5%").

Bands:
- **High**: score ≥ 70
- **Medium**: 40 ≤ score < 70
- **Low**: score < 40
