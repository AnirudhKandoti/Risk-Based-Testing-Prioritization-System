from sqlalchemy.orm import Session
from datetime import datetime, timezone
from . import models

def upsert_module(db: Session, name: str, owner: str | None, domain: str | None):
    m = db.query(models.Module).filter(models.Module.name == name).one_or_none()
    if not m:
        m = models.Module(name=name, owner=owner, domain=domain)
        db.add(m)
        db.flush()
    else:
        if owner: m.owner = owner
        if domain: m.domain = domain
    return m

def add_events(db: Session, module: models.Module, events: list[dict]):
    for e in events:
        at = e.get("at")
        if at is None:
            at = datetime.now(timezone.utc)
        ev = models.TelemetryEvent(module_id=module.id, kind=e["kind"], value=float(e["value"]), at=at)
        db.add(ev)
    db.flush()
