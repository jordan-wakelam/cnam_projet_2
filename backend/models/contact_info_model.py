
from datetime import time
from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, Time
from sqlalchemy.orm import relationship
from typing import Optional


class PublicationSchedule(Base):
    __tablename__ = 'publication_schedule'

    # Utilisation de Mapped pour la déclaration des colonnes
    publication: Mapped[str] = mapped_column(String(100), primary_key=True)
    day: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[time] = mapped_column(Time, primary_key=True)
    end: Mapped[Optional[time]] = mapped_column(Time)

    # Relation avec ScheduleTimes
    schedule_times = relationship("ScheduleTimes", back_populates="schedule")

    def __repr__(self):
        return f"<PublicationSchedule(publication={self.publication}, day={self.day}, start={self.start}, end={self.end})>"
