
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .import Base

class PublicationContact(Base):
    __tablename__ = 'publication_contact'

    publication = Column(String(100), primary_key=True)
    lastname = Column(String(50), ForeignKey('contact_id.lastname'), primary_key=True)
    firstname = Column(String(50), ForeignKey('contact_id.firstname'), primary_key=True)
    type = Column(String(20))
    value = Column(String(50))
    id = Column(Integer, ForeignKey('contact_info.id'))

    contact = relationship("ContactId", back_populates="publications")
    info = relationship("ContactInfo", back_populates="publication_contact")