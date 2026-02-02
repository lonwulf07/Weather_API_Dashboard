from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Integer)
    condition = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)