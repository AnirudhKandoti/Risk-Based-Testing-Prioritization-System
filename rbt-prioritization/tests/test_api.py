from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_ingest_and_priorities():
    client = TestClient(app)
    payload = {
        "module_name":"checkout",
        "events":[
            {"kind":"error_rate","value":0.08},
            {"kind":"change_frequency","value":8},
            {"kind":"code_churn","value":900},
            {"kind":"complexity","value":0.7},
            {"kind":"customer_impact","value":0.8},
            {"kind":"sla_breaches","value":1},
            {"kind":"test_flakiness","value":0.2},
        ]
    }
    r = client.post("/ingest/telemetry", json=payload)
    assert r.status_code == 200

    r2 = client.get("/priorities")
    assert r2.status_code == 200
    data = r2.json()
    assert len(data["items"]) >= 1
    item = data["items"][0]
    assert "score" in item and "contributions" in item
