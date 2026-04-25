from fastapi import FastAPI
from app.schemas.telemetry import Telemetry

app = FastAPI()

@app.post('/ingest/')
async def add_telemetry(telemetry: Telemetry):
    return {"status": "ok"}