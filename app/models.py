from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    email_token = Column(String)
    api_token = Column(String)
    is_active = Column(Boolean, default=False)

