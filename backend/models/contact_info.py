
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class ContactInfo(Base):
    __tablename__ = 'contact_info'

    id = Column(Integer, primary_key=True)
    type = Column(String(20))
    value = Column(String(50))

    publication_contact = relationship("PublicationContact", back_populates="info")