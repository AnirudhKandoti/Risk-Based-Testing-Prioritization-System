from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class TelemetryPoint(BaseModel):
    kind: str
    value: float
    at: Optional[datetime] = None

class TelemetryIngest(BaseModel):
    module_name: str = Field(..., examples=["checkout"])
    owner: Optional[str] = None
    domain: Optional[str] = None
    events: List[TelemetryPoint]

class ModuleOut(BaseModel):
    name: str
    owner: Optional[str] = None
    domain: Optional[str] = None
    last_change_at: Optional[datetime] = None

class RiskOut(BaseModel):
    module_name: str
    score: float
    band: str
    contributions: Dict[str, float]
    reasons: List[str]

class PriorityOut(BaseModel):
    items: List[RiskOut]
