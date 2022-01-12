from fastapi import FastAPI,Request
from pydantic import BaseModel

from app.config import Config
from app.models import *

from typing import Dict

from typing import List

from pydantic import BaseModel, Json, ValidationError
import json


# from datetime import datetime
class CanceledServiceData(BaseModel):
    m_metro_export_trip_id: int
    stop_description_first: str
    stop_description_last: str
    trip_time_start: str
    trip_time_end: str
    type: str
    


app = FastAPI()

@app.get("/canceled_service/{trip_type}")
async def get_body(trip_type):
    with open('../data/CancelledTripsRT.json', 'r') as file:
        cancelled_service_json = json.loads(file.read())
        canceled_service = []
        for row in cancelled_service_json["CanceledService"]:
            if row["trp_type"] == trip_type:
                canceled_service.append(CanceledServiceData(m_metro_export_trip_id=row["m_metro_export_trip_id"],
                                                stop_description_first=row["stop_description_first"],
                                                stop_description_last=row["stop_description_last"],
                                                trip_time_start=row["trp_time_start"],
                                                trip_time_end=row["trp_time_end"],
                                                type=row["trp_type"]))
    return {"canceled_data":canceled_service}

@app.get("/")
async def root():
    
    return {"Nina": "Hello World!"}