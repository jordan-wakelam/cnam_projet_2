
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models import ContactId

class ContactIdDTO(BaseModel):
    firstname: str
    lastname: str
    publications_count: Optional[int] = Field(None, alias="publicationsCount")

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model

    def to_dict(self) -> dict:
        """Returns the object as a dictionary, excluding sensitive fields if needed"""
        return self.model_dump()

# Function to convert ContactId SQLAlchemy model to DTO
def contact_id_to_dto(contact_id: ContactId) -> ContactIdDTO:
    # Calculate the number of publications (assuming it's a list of publications)
    publications_count = len(contact_id.publications) if contact_id.publications else 0

    return ContactIdDTO(
        firstname=contact_id.firstname,
        lastname=contact_id.lastname,
        publications_count=publications_count
    )
