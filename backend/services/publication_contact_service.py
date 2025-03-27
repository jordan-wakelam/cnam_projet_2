from sqlalchemy.orm import Session
from models.publication_contact_model import PublicationContact  # Modèle PublicationContact
from dtos.publication_contact_dto import PublicationContactDTO  # DTO PublicationContact
from models import create_session_local
from datetime import datetime


def insert_publication_contact(
        publication_contact_dto: PublicationContactDTO) -> PublicationContact:
    """Insère une nouvelle entrée dans la table PublicationContact à partir d'un DTO.

    Args:
        publication_contact_dto (PublicationContactDTO): L'objet DTO contenant les informations de publication contact.

    Returns:
        PublicationContact: L'objet PublicationContact inséré dans la base de données.
    """
    session = create_session_local()  # Créer une session locale
    try:
        new_publication_contact = PublicationContact(
            publication=publication_contact_dto.publication,
            lastname=publication_contact_dto.lastname,
            firstname=publication_contact_dto.firstname,
            type=publication_contact_dto.type,
            value=publication_contact_dto.value,
            id=publication_contact_dto.
            id  # Supposons que l'ID de contact_info existe déjà
        )

        session.add(new_publication_contact)
        session.commit()
        session.refresh(new_publication_contact
                        )  # Rafraîchir pour obtenir les valeurs actuelles
        return new_publication_contact
    except Exception as e:
        session.rollback()
        raise ValueError(
            f"Erreur lors de l'insertion de la publication contact : {str(e)}")
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def get_publication_contact(publication: str, lastname: str,
                            firstname: str) -> PublicationContact:
    """Récupère un contact de publication en fonction de la publication, du nom et du prénom.

    Args:
        publication (str): Le nom de la publication.
        lastname (str): Le nom du contact.
        firstname (str): Le prénom du contact.

    Returns:
        PublicationContact: Le contact de publication trouvé ou None si non trouvé.
    """
    session = create_session_local()  # Créer une session locale
    try:
        publication_contact = session.query(PublicationContact).filter_by(
            publication=publication, lastname=lastname,
            firstname=firstname).first()

        return publication_contact  # Retourner le contact de publication trouvé, ou None si pas trouvé.

    except Exception as e:
        print(
            f"Erreur lors de la récupération du contact de publication : {str(e)}"
        )
        return None
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def update_publication_contact(
        publication: str, lastname: str, firstname: str,
        publication_contact_dto: PublicationContactDTO) -> PublicationContact:
    """Met à jour un contact de publication existant.

    Args:
        publication (str): Le nom de la publication du contact.
        lastname (str): Le nom du contact à mettre à jour.
        firstname (str): Le prénom du contact à mettre à jour.
        publication_contact_dto (PublicationContactDTO): Les nouvelles informations de contact de publication.

    Returns:
        PublicationContact: Le contact de publication mis à jour.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de la publication_contact à mettre à jour
        publication_contact = session.query(PublicationContact).filter_by(
            publication=publication, lastname=lastname,
            firstname=firstname).first()

        if not publication_contact:
            raise ValueError(
                f"Contact de publication avec publication {publication}, lastname {lastname}, firstname {firstname} non trouvé."
            )

        # Mise à jour des champs
        if publication_contact_dto.type:
            publication_contact.type = publication_contact_dto.type
        if publication_contact_dto.value:
            publication_contact.value = publication_contact_dto.value
        if publication_contact_dto.id:
            publication_contact.id = publication_contact_dto.id  # Mettre à jour l'ID de ContactInfo si nécessaire

        # Sauvegarde des modifications
        session.commit()
        session.refresh(
            publication_contact
        )  # Rafraîchir l'objet pour obtenir les valeurs mises à jour

        return publication_contact  # Retourner le contact de publication mis à jour

    except Exception as e:
        session.rollback()
        raise ValueError(
            f"Erreur lors de la mise à jour du contact de publication : {str(e)}"
        )

    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def delete_publication_contact(publication: str, lastname: str,
                               firstname: str) -> bool:
    """Supprime un contact de publication de la base de données.

    Args:
        publication (str): Le nom de la publication.
        lastname (str): Le nom du contact à supprimer.
        firstname (str): Le prénom du contact à supprimer.

    Returns:
        bool: Retourne True si la suppression est réussie, False sinon.
    """
    session = create_session_local()  # Créer une session locale
    try:
        publication_contact = session.query(PublicationContact).filter_by(
            publication=publication, lastname=lastname,
            firstname=firstname).first()

        if not publication_contact:
            raise ValueError(
                f"Contact de publication avec publication {publication}, lastname {lastname}, firstname {firstname} non trouvé."
            )

        session.delete(publication_contact)
        session.commit()
        return True  # Retourner True si la suppression est réussie
    except Exception as e:
        session.rollback()
        print(
            f"Erreur lors de la suppression du contact de publication : {str(e)}"
        )
        return False
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin
