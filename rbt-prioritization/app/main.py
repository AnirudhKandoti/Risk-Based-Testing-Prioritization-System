from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import telemetry, priorities, modules

app = FastAPI(title="Risk-Based Testing Prioritization System")

app.include_router(telemetry.router)
app.include_router(priorities.router)
app.include_router(modules.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home(request: Request):
    # Fetch priorities from internal endpoint to show in UI
    # (In larger systems, you would inject a service.)
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/priorities?limit=200")
    data = resp.json()
    return templates.TemplateResponse("index.html", {"request": request, "items": data["items"]})

@app.get("/ui/modules/{name}")
def ui_module(name: str, request: Request):
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get(f"/modules/{name}")
    data = resp.json()
    return templates.TemplateResponse("module_detail.html", {"request": request, **data})
