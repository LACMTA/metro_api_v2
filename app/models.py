from pydantic import BaseModel, Json, ValidationError
from app.config import Config

class CanceledServiceData(BaseModel):
    m_metro_export_trip_id: int
    trp_route: int
    stop_description_first: str
    stop_description_last: str
    trip_time_start: str
    trip_time_end: str
    type: str


