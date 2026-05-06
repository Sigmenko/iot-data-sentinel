import requests
from datetime import datetime
import random
import time

url = "http://127.0.0.1:8000/ingest/"
while True:
    data = {
        'device_id': 'test_esp',
        'temperature': round(random.uniform(15.0,30.0), 2),
        'humidity': round(random.uniform(10.0, 99.00), 2),
        'timestamp': datetime.now().isoformat()
    }

    r = requests.post(url=url, json=data)
    print(f"status code {r.status_code}")
    print(f"response {r.json()}")
    time.sleep(0.5)
