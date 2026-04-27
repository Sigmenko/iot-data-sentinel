from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.db.database import Base

class TelemetryRecord(Base):
    __tablename__ = "telemetry_data"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime)
    is_critical = Column(Boolean)