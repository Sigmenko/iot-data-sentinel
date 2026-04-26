from fastapi import FastAPI
from app.schemas.telemetry import Telemetry
from app.services.data_processor import data_proces

app = FastAPI()

@app.post('/ingest/')
async def add_telemetry(telemetry: Telemetry):
    return data_proces(telemetry)