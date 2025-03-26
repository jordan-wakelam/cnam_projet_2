
from sqlalchemy import Column, String, Integer, Time
from sqlalchemy.orm import relationship
from .import Base

class PublicationSchedule(Base):
    __tablename__ = 'publication_schedule'

    publication = Column(String(100), primary_key=True)
    day = Column(Integer, primary_key=True)
    start = Column(Time, primary_key=True)
    end = Column(Time)

    schedule_times = relationship("ScheduleTimes", back_populates="schedule")