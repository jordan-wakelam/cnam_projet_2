
from sqlalchemy.orm import Session
from backend.models.contact_id_model import ContactId  # Modèle ContactId
from dtos.contact_id_dto import ContactIdDTO  # DTO ContactId
from models import create_session_local


def insert_contact_id(contact_id_dto: ContactIdDTO) -> ContactId:
    """Insère un nouveau contact dans la table ContactId à partir d'un DTO.

    Args:
        contact_id_dto (ContactIdDTO): L'objet DTO contenant les informations du contact.

    Returns:
        ContactId: L'objet ContactId inséré dans la base de données.
    """
    session = create_session_local()  # Créer une session locale
    try:
        new_contact_id = ContactId(
            lastname=contact_id_dto.lastname,
            firstname=contact_id_dto.firstname
        )

        session.add(new_contact_id)
        session.commit()
        session.refresh(new_contact_id)  # Rafraîchir pour obtenir les valeurs actuelles
        return new_contact_id
    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de l'insertion du contact ID : {str(e)}")
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def get_contact_id(lastname: str, firstname: str) -> ContactId:
    """Récupère un contact en fonction du nom et du prénom.

    Args:
        lastname (str): Le nom du contact.
        firstname (str): Le prénom du contact.

    Returns:
        ContactId: Le contact trouvé ou None si non trouvé.
    """
    session = create_session_local()  # Créer une session locale
    try:
        contact_id = session.query(ContactId).filter_by(
            lastname=lastname,
            firstname=firstname
        ).first()

        return contact_id  # Retourner le contact trouvé, ou None si pas trouvé.

    except Exception as e:
        print(f"Erreur lors de la récupération du contact ID : {str(e)}")
        return None
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def update_contact_id(lastname: str, firstname: str, contact_id_dto: ContactIdDTO) -> ContactId:
    """Met à jour un contact ID existant.

    Args:
        lastname (str): Le nom du contact à mettre à jour.
        firstname (str): Le prénom du contact à mettre à jour.
        contact_id_dto (ContactIdDTO): Les nouvelles informations de contact.

    Returns:
        ContactId: Le contact ID mis à jour.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche du contact à mettre à jour
        contact_id = session.query(ContactId).filter_by(
            lastname=lastname,
            firstname=firstname
        ).first()

        if not contact_id:
            raise ValueError(f"Contact avec lastname {lastname}, firstname {firstname} non trouvé.")

        # Mise à jour des champs
        if contact_id_dto.lastname:
            contact_id.lastname = contact_id_dto.lastname
        if contact_id_dto.firstname:
            contact_id.firstname = contact_id_dto.firstname

        # Sauvegarde des modifications
        session.commit()
        session.refresh(contact_id)  # Rafraîchir l'objet pour obtenir les valeurs mises à jour

        return contact_id  # Retourner le contact mis à jour

    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de la mise à jour du contact ID : {str(e)}")

    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def delete_contact_id(lastname: str, firstname: str) -> bool:
    """Supprime un contact de la base de données.

    Args:
        lastname (str): Le nom du contact à supprimer.
        firstname (str): Le prénom du contact à supprimer.

    Returns:
        bool: Retourne True si la suppression est réussie, False sinon.
    """
    session = create_session_local()  # Créer une session locale
    try:
        contact_id = session.query(ContactId).filter_by(
            lastname=lastname,
            firstname=firstname
        ).first()

        if not contact_id:
            raise ValueError(f"Contact avec lastname {lastname}, firstname {firstname} non trouvé.")

        session.delete(contact_id)
        session.commit()
        return True  # Retourner True si la suppression est réussie
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression du contact ID : {str(e)}")
        return False
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin
