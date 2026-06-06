import hashlib
from datetime import datetime
from app.db.models import HubDevice, SatTelemetryDHT11


def load_telemetry_to_vault(db_session, mac_address: str, temperature: float, humidity: float, timestamp: datetime):
    """
    ETL function
    """
    #xxxешування
    hash_input = mac_address.encode('utf-8')
    device_hash = hashlib.md5(hash_input).hexdigest()

    # hubs
    existing_hub = db_session.query(HubDevice).filter_by(device_hash_key=device_hash).first()
    if not existing_hub:
        new_hub = HubDevice(
            device_hash_key=device_hash,
            load_data=datetime.now(),
            source_data="ESP32_API",
            device_id=mac_address
        )
        db_session.add(new_hub)
        db_session.flush()

    # SATELLITE
    new_satellite = SatTelemetryDHT11(
        device_hash_key=device_hash,
        load_data=timestamp,
        source_data="ESP32_API",
        temperature=temperature,
        humidity=humidity
    )
    db_session.add(new_satellite)

