import datetime
from sqlalchemy import Column, String, Integer, DateTime

from app.db.base_class import Base

class Feedback(Base):
    id = Column(Integer(), primary_key=True, autoincrement=True)
    frustrations = Column(String(2048))
    suggestions = Column(String(2048))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
