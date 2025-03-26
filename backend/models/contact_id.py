
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from . import Base

class ContactId(Base):
    __tablename__ = 'contact_id'

    lastname = Column(String(50), primary_key=True)
    firstname = Column(String(50), primary_key=True)

    publications = relationship("PublicationContact", back_populates="contact")