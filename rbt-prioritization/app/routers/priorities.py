from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..database import get_db
from .. import models, schemas
from ..prioritizer import compute_score, band_for, make_reasons

router = APIRouter(prefix="/priorities", tags=["priorities"])

def _aggregate_features(db, module_id: int) -> dict:
    # Aggregate latest window by simple reductions (last/avg/sum as sensible defaults).
    # In real deployment, use windowing (e.g., 14d) and metrics store.
    rows = db.execute(
        select(models.TelemetryEvent.kind, func.avg(models.TelemetryEvent.value))
        .where(models.TelemetryEvent.module_id == module_id)
        .group_by(models.TelemetryEvent.kind)
    ).all()
    feats = {k: float(v or 0.0) for k, v in rows}
    # Ensure all features exist:
    for k in ["error_rate","change_frequency","code_churn","complexity","customer_impact","sla_breaches","test_flakiness"]:
        feats.setdefault(k, 0.0)
    return feats

@router.get("", response_model=schemas.PriorityOut)
def get_priorities(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db)):
    modules = db.query(models.Module).order_by(models.Module.name).limit(limit).all()
    items = []
    for m in modules:
        feats = _aggregate_features(db, m.id)
        score, contribs = compute_score(feats)
        band = band_for(score)
        reasons = make_reasons(feats)
        items.append({"module_name": m.name, "score": score, "band": band, "contributions": contribs, "reasons": reasons})
    # sort by score desc
    items.sort(key=lambda x: x["score"], reverse=True)
    return {"items": items}

@router.post("/recompute")
def recompute_and_persist(db: Session = Depends(get_db)):
    modules = db.query(models.Module).all()
    created = 0
    for m in modules:
        feats = _aggregate_features(db, m.id)
        score, contribs = compute_score(feats)
        band = band_for(score)
        snap = models.RiskSnapshot(module_id=m.id, score=score, band=band, contributions=contribs)
        db.add(snap)
        created += 1
    db.commit()
    return {"status": "ok", "snapshots": created}
