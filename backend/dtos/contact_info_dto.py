
from pydantic import BaseModel, Field
from typing import Optional
from models.contact_info_model import ContactInfo  # Assurez-vous que ce modèle existe dans votre projet

class ContactInfoDTO(BaseModel):
    type: Optional[str] = None
    value: Optional[str] = None

    class Config:
        from_attributes = True  # Permet de convertir depuis un modèle SQLAlchemy

    def to_dict(self) -> dict:
        """Retourne l'objet sous forme de dictionnaire"""
        return self.model_dump()

# Exemple d'utilisation pour convertir un objet ContactInfo SQLAlchemy en DTO
def contact_info_to_dto(contact_info: ContactInfo) -> ContactInfoDTO:
    return ContactInfoDTO(
        type=contact_info.type,
        value=contact_info.value
    )
