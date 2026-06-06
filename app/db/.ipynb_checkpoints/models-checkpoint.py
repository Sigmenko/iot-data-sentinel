from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from app.db.database import Base
import hashlib

class TelemetryRecord(Base):
    __tablename__ = "telemetry_data"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime)
    is_critical = Column(Boolean)


#Implementation Data Vault 2.0
# hub - лише унікальні індефікатори пристроїв
class HubDevice(Base):
    __tablename__ = "device_hub"
    device_hash_key = Column(String, primary_key=True)
    load_data = Column(DateTime, nullable=False) # when we get this record(time)
    source_data = Column(String, nullable=False) # from we get this record

    #business_key(real mac-adress)
    device_id = Column(String, unique=True, nullable=False)

# SATELLITE - контекст і самі показники
class SatTelemetryDHT11(Base):
    __tablename__ = "sat_telemetry_dht11"

    # Складений первинний ключ: Хеш Хаба + Час завантаження
    device_hash_key = Column(String, ForeignKey('device_hub.device_hash_key'), primary_key=True)
    load_data = Column(DateTime, nullable=False)
    source_data = Column(String, nullable=False)

    temperature = Column(Float)
    humidity = Column(Float)