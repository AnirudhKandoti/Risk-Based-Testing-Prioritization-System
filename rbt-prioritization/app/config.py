from dataclasses import dataclass

@dataclass
class RiskWeights:
    error_rate: float = 5.0
    change_frequency: float = 4.0
    code_churn: float = 3.0
    complexity: float = 2.0
    customer_impact: float = 4.0
    sla_breaches: float = 3.0
    test_flakiness: float = 2.0

DEFAULT_WEIGHTS = RiskWeights()

# Feature normalization caps (values beyond cap treated as cap)
NORMALIZATION_CAPS = {
    "error_rate": 0.2,         # 20% errors
    "change_frequency": 14.0,  # changes / 14 days
    "code_churn": 2000.0,      # lines changed window
    "complexity": 1.0,         # already 0..1
    "customer_impact": 1.0,    # 0..1 proxy
    "sla_breaches": 10.0,      # recent breaches
    "test_flakiness": 0.5,     # 50% flaky
}

BANDS = [
    ("High", 70),
    ("Medium", 40),
    ("Low", 0),
]
