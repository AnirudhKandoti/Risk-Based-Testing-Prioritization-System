from app.prioritizer import compute_score, band_for

def test_compute_score_monotonic():
    base = {
        "error_rate": 0.0,
        "change_frequency": 0.0,
        "code_churn": 0.0,
        "complexity": 0.0,
        "customer_impact": 0.0,
        "sla_breaches": 0.0,
        "test_flakiness": 0.0,
    }
    s0, _ = compute_score(base)
    high = base | {"error_rate": 0.2, "change_frequency": 14, "code_churn": 2000, "complexity": 1.0, "customer_impact": 1.0, "sla_breaches": 10, "test_flakiness": 0.5}
    s1, _ = compute_score(high)
    assert s1 > s0
    assert 0.0 <= s0 <= 100.0
    assert 0.0 <= s1 <= 100.0

def test_bands():
    assert band_for(85) == "High"
    assert band_for(55) == "Medium"
    assert band_for(15) == "Low"
