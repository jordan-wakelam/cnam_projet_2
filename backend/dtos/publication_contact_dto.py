
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime
import re
from models import PublicationContact  # Importer le modèle PublicationContact de SQLAlchemy

class PublicationContactDTO(BaseModel):
    publication: str
    lastname: str
    firstname: str
    type: Optional[str] = None
    value: Optional[str] = None
    id: Optional[int] = None

    class Config:
        from_attributes = True  # Permet de convertir depuis un modèle SQLAlchemy

    def to_dict(self) -> dict:
        """Retourne l'objet sous forme de dictionnaire"""
        return self.model_dump()

    @model_validator(mode='before')
    def validate_type(cls, values):
        """Validation pour le type de publication, si nécessaire"""
        type_ = values.get('type')
        if type_ and len(type_) > 20:
            raise ValueError("Type must be at most 20 characters long.")
        return values

# Exemple d'utilisation pour convertir un objet PublicationContact SQLAlchemy en DTO
def publication_contact_to_dto(publication_contact: PublicationContact) -> PublicationContactDTO:
    return PublicationContactDTO(
        publication=publication_contact.publication,
        lastname=publication_contact.lastname,
        firstname=publication_contact.firstname,
        type=publication_contact.type,
        value=publication_contact.value,
        id=publication_contact.id
    )
