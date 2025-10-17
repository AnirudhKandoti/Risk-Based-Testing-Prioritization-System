from typing import Dict, Tuple, List
from .config import DEFAULT_WEIGHTS, NORMALIZATION_CAPS, BANDS
import math

def _clip(value: float, cap: float) -> float:
    if cap <= 0:
        return 0.0
    return max(0.0, min(value, cap))

def _normalize(value: float, cap: float) -> float:
    return _clip(value, cap) / cap if cap > 0 else 0.0

def compute_score(features: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
    """Compute total risk score [0..100] and per-feature contributions."""
    weights = DEFAULT_WEIGHTS.__dict__
    total_w = sum(weights.values())
    contribs: Dict[str, float] = {}
    num = 0.0
    for k, w in weights.items():
        v = features.get(k, 0.0)
        norm = _normalize(v, NORMALIZATION_CAPS.get(k, 1.0))
        c = 100.0 * w * norm / total_w
        contribs[k] = round(c, 2)
        num += w * norm
    score = 100.0 * num / total_w
    return round(score, 2), contribs

def band_for(score: float) -> str:
    for name, threshold in BANDS:
        if score >= threshold:
            return name
    return "Low"

def make_reasons(features: Dict[str, float]) -> List[str]:
    reasons = []
    # Simple threshold-based rationales
    if features.get("error_rate", 0) > 0.05:
        reasons.append("Elevated error_rate (>5%).")
    if features.get("change_frequency", 0) > 7:
        reasons.append("Frequent changes this sprint (change_frequency > 7).")
    if features.get("code_churn", 0) > 800:
        reasons.append("High code churn in recent window (>800 LOC).")
    if features.get("complexity", 0) > 0.6:
        reasons.append("Module complexity above recommended threshold (>0.6).")
    if features.get("customer_impact", 0) > 0.7:
        reasons.append("High customer impact (top-tier users).")
    if features.get("sla_breaches", 0) >= 1:
        reasons.append("Recent SLA breaches detected.")
    if features.get("test_flakiness", 0) > 0.15:
        reasons.append("Flaky tests observed (>15%).")
    if not reasons:
        reasons.append("No standout risk drivers; monitoring at routine level.")
    return reasons
