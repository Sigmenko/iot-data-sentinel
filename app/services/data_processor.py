from typing import Dict
import pandas as pd
from app.schemas.telemetry import Telemetry


def data_proces(data: Telemetry) -> Dict:
    data_dict = data.model_dump()
    df = pd.DataFrame([data_dict])

    df['is_critical'] = df['temperature'] > 30

    result_dict = df.to_dict(orient="records")[0]

    return result_dict
