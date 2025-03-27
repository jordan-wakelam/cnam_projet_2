
from datetime import time
from sqlalchemy import Integer, Time, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from . import Base
from .publication_schedule_model import PublicationSchedule

class ScheduleTimes(Base):
    __tablename__ = 'schedule_times'

    day: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[time] = mapped_column(Time, primary_key=True)
    end: Mapped[time] = mapped_column(Time, nullable=False)

    schedule: Mapped[List["PublicationSchedule"]] = relationship("PublicationSchedule", back_populates="schedule_times")

    def __repr__(self):
        return f"<ScheduleTimes(day={self.day}, start={self.start}, end={self.end})>"
