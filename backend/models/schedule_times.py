
from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class ScheduleTimes(Base):
    __tablename__ = 'schedule_times'

    day = Column(Integer, primary_key=True)
    start = Column(Time, primary_key=True)
    end = Column(Time, primary_key=True)

    schedule = relationship("PublicationSchedule", back_populates="schedule_times")