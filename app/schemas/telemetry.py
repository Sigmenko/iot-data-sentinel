from pydantic import BaseModel, Field
from datetime import datetime

class Telemetry(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=15)
    temperature: float = Field(..., ge=-50.0, le=70.0, description='temperature must between -50 and 70')
    humidity: float = Field(..., ge=0.0, le=100.0, description='humidity must be 1-100')
    timestamp: datetime