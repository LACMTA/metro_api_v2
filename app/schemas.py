from typing import Optional
from pydantic import BaseModel, Json, ValidationError

from .config import Config

class EmailVerifyToken(BaseModel):
    email_address: str
    # email_token: str
    # token_type: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    username: str
    password: str
    # email_token: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str

class CanceledServiceData(BaseModel):
    gtfs_trip_id: str
    trip_route: str
    stop_description_first: str
    stop_description_last: str
    trip_time_start: str
    trip_time_end: str
    trip_direction: str


