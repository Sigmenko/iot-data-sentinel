from fastapi import FastAPI
from app.schemas.telemetry import Telemetry
from app.services.data_processor import data_proces
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import engine, get_db
from sqlalchemy import func
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
@app.get('/telemetry/')
async def get_last_telemetry(db: Session = Depends(get_db)):
    record = db.query(models.TelemetryRecord).order_by(models.TelemetryRecord.id.desc()).limit(5).all()
    return record

@app.get('/analytic/')
async def analysis(db: Session = Depends(get_db)):
    avg_temp, max_hum, count_records = db.query(
        func.avg(models.TelemetryRecord.temperature),
        func.max(models.TelemetryRecord.humidity),
        func.count(models.TelemetryRecord.id)
    ).first()
    return {
        'total count records': count_records,
        'avg temperature': avg_temp,
        'max humidity': max_hum
    }