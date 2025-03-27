
from datetime import time
from sqlalchemy import Integer, Time, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List, TYPE_CHECKING
from . import Base

if TYPE_CHECKING:
    from .schedule_times_model import ScheduleTimes

class PublicationSchedule(Base):
    __tablename__ = 'publication_schedule'

    publication: Mapped[str] = mapped_column(String(100), primary_key=True)
    day: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[time] = mapped_column(Time, primary_key=True)
    end: Mapped[time] = mapped_column(Time, nullable=False)

    schedule_times: Mapped[List["ScheduleTimes"]] = relationship("ScheduleTimes", back_populates="schedule")

    def __repr__(self):
        return f"<PublicationSchedule(publication={self.publication}, day={self.day}, start={self.start}, end={self.end})>"
