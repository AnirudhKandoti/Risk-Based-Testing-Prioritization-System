from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..prioritizer import compute_score, band_for, make_reasons
from ..explainability import rank_contributions

router = APIRouter(prefix="/modules", tags=["modules"])

@router.get("/{name}")
def module_detail(name: str, db: Session = Depends(get_db)):
    m = db.query(models.Module).filter(models.Module.name == name).one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail="Module not found")
    # Aggregate on the fly for simplicity
    feats = {}
    for ev in m.telemetry:
        feats.setdefault(ev.kind, []).append(ev.value)
    feats = {k: sum(v)/len(v) for k,v in feats.items()}
    score, contribs = compute_score(feats)
    band = band_for(score)
    reasons = make_reasons(feats)
    ranked = rank_contributions(contribs)
    return {
        "module": {"name": m.name, "owner": m.owner, "domain": m.domain},
        "features": feats,
        "score": score,
        "band": band,
        "contributions": contribs,
        "ranked_contributions": ranked,
        "reasons": reasons,
    }
