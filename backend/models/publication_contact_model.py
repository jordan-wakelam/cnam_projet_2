from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from . import Base
from typing import Optional
# from models.contact_id_model import ContactId
# from models.contact_info_model import ContactInfo


class PublicationContact(Base):
    __tablename__ = 'publication_contact'

    publication: Mapped[str] = mapped_column("publication",
                                             String(100),
                                             primary_key=True)
    lastname: Mapped[str] = mapped_column("lastname",
                                          String(50),
                                          ForeignKey('contact_id.lastname'),
                                          primary_key=True)
    firstname: Mapped[str] = mapped_column("firstname",
                                           String(50),
                                           ForeignKey('contact_id.firstname'),
                                           primary_key=True)
    type: Mapped[Optional[str]] = mapped_column("type", String(20))
    value: Mapped[Optional[str]] = mapped_column("value", String(50))
    id: Mapped[Optional[int]] = mapped_column("id", Integer,
                                              ForeignKey('contact_info.id'))

    contact: Mapped['ContactId'] = relationship("ContactId",
                                                back_populates="publications")
    info: Mapped['ContactInfo'] = relationship(
        "ContactInfo", back_populates="publication_contact")

    def __init__(self,
                 publication: str,
                 lastname: str,
                 firstname: str,
                 type: Optional[str] = None,
                 value: Optional[str] = None,
                 id: Optional[int] = None):
        """
        Constructeur de la classe PublicationContact.
        
        :param publication: Le nom de la publication.
        :param lastname: Le nom de famille du contact.
        :param firstname: Le prénom du contact.
        :param type: Le type de contact (optionnel).
        :param value: La valeur du contact (optionnel).
        :param id: L'id du contact associé (optionnel).
        """
        self.publication = publication
        self.lastname = lastname
        self.firstname = firstname
        self.type = type
        self.value = value
        self.id = id

    def __repr__(self):
        return (
            f'<PublicationContact(publication={self.publication}, lastname={self.lastname}, '
            f'firstname={self.firstname}, type={self.type}, value={self.value}, id={self.id})>'
        )
