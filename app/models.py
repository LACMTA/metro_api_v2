from pydantic import BaseModel, Json, ValidationError
from app.config import Config

class CanceledServiceData(BaseModel):
    gtfs_trip_id: str
    trip_route: str
    stop_description_first: str
    stop_description_last: str
    trip_time_start: str
    trip_time_end: str
    trip_direction: str


