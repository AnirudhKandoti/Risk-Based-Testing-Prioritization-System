from typing import Dict, List
# For this simple explainer, we just echo the contributions and add reasons (see prioritizer).
# You could swap this with SHAP/LIME or rulefit without changing the API.

def rank_contributions(contribs: Dict[str, float]) -> List[str]:
    return [k for k, _ in sorted(contribs.items(), key=lambda kv: kv[1], reverse=True)]
