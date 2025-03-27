from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from . import Base
from typing import Optional
# from models.publication_contact_model import PublicationContact


class ContactId(Base):
    __tablename__ = 'contact_id'

    lastname: Mapped[str] = mapped_column("lastname",
                                          String(50),
                                          primary_key=True)
    firstname: Mapped[str] = mapped_column("firstname",
                                           String(50),
                                           primary_key=True)

    publications: Mapped[Optional["PublicationContact"]] = relationship(
        "PublicationContact", back_populates="contact")

    def __repr__(self):
        return f'<ContactId(firstname={self.firstname}, lastname={self.lastname})>'
