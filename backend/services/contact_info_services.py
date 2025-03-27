
from sqlalchemy.orm import Session
from models.contact_info_model import ContactInfo
from dtos.contact_info_dto import ContactInfoDTO
from models import create_session_local  # Assurez-vous d'importer correctement cette fonction
from typing import Optional


def insert_contact_info(contact_info_dto: ContactInfoDTO) -> ContactInfo:
    """Insère des informations de contact dans la base de données à partir d'un DTO.

    Args:
        contact_info_dto (ContactInfoDTO): L'objet DTO contenant les informations de contact.

    Returns:
        ContactInfo: L'objet ContactInfo inséré en base de données.
    """
    session = create_session_local()  # Créer une session locale
    try:
        new_contact_info = ContactInfo(
            type=contact_info_dto.type,
            value=contact_info_dto.value
        )

        session.add(new_contact_info)
        session.commit()
        session.refresh(new_contact_info)  # Rafraîchir pour récupérer les nouvelles valeurs
        return new_contact_info
    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de l'insertion des informations de contact : {str(e)}")
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def get_contact_info_by_id(contact_info_id: int) -> Optional[ContactInfo]:
    """Récupère les informations de contact en fonction de l'ID.

    Args:
        contact_info_id (int): L'ID des informations de contact à récupérer.

    Returns:
        ContactInfo: L'objet ContactInfo trouvé ou None si l'objet n'existe pas.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de l'information de contact par ID
        contact_info = session.query(ContactInfo).filter_by(id=contact_info_id).first()

        return contact_info  # Retourne l'objet trouvé ou None si pas trouvé.
    except Exception as e:
        print(f"Erreur lors de la récupération des informations de contact : {str(e)}")
        return None
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def update_contact_info(contact_info_id: int, contact_info_dto: ContactInfoDTO) -> ContactInfo:
    """Met à jour les informations de contact à partir d'un DTO.

    Args:
        contact_info_id (int): L'ID des informations de contact à mettre à jour.
        contact_info_dto (ContactInfoDTO): L'objet DTO contenant les nouvelles informations de contact.

    Returns:
        ContactInfo: L'objet ContactInfo mis à jour.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de l'information de contact par ID
        contact_info = session.query(ContactInfo).filter_by(id=contact_info_id).first()

        if not contact_info:
            raise ValueError(f"Information de contact avec l'ID {contact_info_id} non trouvée.")

        # Mise à jour des champs de l'information de contact
        if contact_info_dto.type:
            contact_info.type = contact_info_dto.type
        if contact_info_dto.value:
            contact_info.value = contact_info_dto.value

        # Sauvegarde des modifications
        session.commit()
        session.refresh(contact_info)  # Rafraîchir l'objet pour obtenir les valeurs mises à jour

        return contact_info  # Retourner l'objet mis à jour
    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de la mise à jour des informations de contact : {str(e)}")
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def delete_contact_info(contact_info_id: int) -> bool:
    """Supprime des informations de contact de la base de données.

    Args:
        contact_info_id (int): L'ID des informations de contact à supprimer.

    Returns:
        bool: True si l'objet a été supprimé, False sinon.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de l'information de contact par ID
        contact_info = session.query(ContactInfo).filter_by(id=contact_info_id).first()

        if not contact_info:
            raise ValueError(f"Information de contact avec l'ID {contact_info_id} non trouvée.")

        # Suppression de l'information de contact
        session.delete(contact_info)
        session.commit()

        return True  # Retourne True si l'objet a été supprimé avec succès.
    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de la suppression des informations de contact : {str(e)}")
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin
