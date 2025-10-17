import json, random, datetime, os
from app.database import SessionLocal, Base, engine
from app.telemetry_ingest import upsert_module, add_events

Base.metadata.create_all(bind=engine)
db = SessionLocal()

modules = [
    ("checkout", "payments@acme.io", "commerce"),
    ("catalog", "search@acme.io", "discovery"),
    ("auth", "platform@acme.io", "platform"),
    ("notifications", "messaging@acme.io", "engagement"),
    ("reporting", "data@acme.io", "analytics"),
]

def gen(module):
    # plausible signal ranges
    return [
        {"kind": "error_rate", "value": random.uniform(0.0, 0.12)},
        {"kind": "change_frequency", "value": random.randint(0, 12)},
        {"kind": "code_churn", "value": random.randint(50, 1600)},
        {"kind": "complexity", "value": random.uniform(0.2, 0.85)},
        {"kind": "customer_impact", "value": random.choice([0.2,0.4,0.6,0.8,0.9])},
        {"kind": "sla_breaches", "value": random.choice([0,0,0,1,2])},
        {"kind": "test_flakiness", "value": random.uniform(0.0, 0.25)},
    ]

for name, owner, domain in modules:
    m = upsert_module(db, name, owner, domain)
    # 10 days of samples
    for d in range(10):
        day = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=10-d)
        evs = gen(name)
        for e in evs:
            e["at"] = day.isoformat()
        add_events(db, m, evs)

db.commit()
db.close()
print("Wrote sample telemetry for", len(modules), "modules.")
