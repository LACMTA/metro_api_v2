from pydantic import BaseModel, Json, ValidationError
from app.config import Config

class CanceledServiceData(BaseModel):
    m_gtfs_trip_id: str
    trp_route: int
    stop_description_first: str
    stop_description_last: str
    trip_time_start: str
    trip_time_end: str
    trip_direction: str


