from fastapi import FastAPI
from app.schemas.telemetry import Telemetry
from app.services.data_processor import data_proces
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import engine, get_db
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post('/ingest/')
async def add_telemetry(telemetry: Telemetry, db: Session = Depends(get_db)):
    processed_data = data_proces(telemetry)
    new_record = models.TelemetryRecord(**processed_data)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record