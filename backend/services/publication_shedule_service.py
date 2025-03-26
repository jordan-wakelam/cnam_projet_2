
from sqlalchemy.orm import Session
from models.publication_schedule import PublicationSchedule  # Modèle PublicationSchedule
from dtos.publication_schedule_dto import PublicationScheduleDTO  # DTO PublicationSchedule
from models import create_session_local
from datetime import datetime


def insert_publication_schedule(publication_schedule_dto: PublicationScheduleDTO) -> PublicationSchedule:
    """Insère un nouvel horaire de publication dans la table PublicationSchedule à partir d'un DTO.

    Args:
        publication_schedule_dto (PublicationScheduleDTO): L'objet DTO contenant les informations de publication schedule.

    Returns:
        PublicationSchedule: L'objet PublicationSchedule inséré dans la base de données.
    """
    session = create_session_local()  # Créer une session locale
    try:
        new_publication_schedule = PublicationSchedule(
            publication=publication_schedule_dto.publication,
            day=publication_schedule_dto.day,
            start=publication_schedule_dto.start,
            end=publication_schedule_dto.end
        )

        session.add(new_publication_schedule)
        session.commit()
        session.refresh(new_publication_schedule)  # Rafraîchir pour obtenir les valeurs actuelles
        return new_publication_schedule
    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de l'insertion de l'horaire de publication : {str(e)}")
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def get_publication_schedule(publication: str, day: int, start: str) -> PublicationSchedule:
    """Récupère un horaire de publication en fonction de la publication, du jour et de l'heure de début.

    Args:
        publication (str): Le nom de la publication.
        day (int): Le jour de la semaine.
        start (str): L'heure de début de la publication.

    Returns:
        PublicationSchedule: L'horaire de publication trouvé ou None si non trouvé.
    """
    session = create_session_local()  # Créer une session locale
    try:
        publication_schedule = session.query(PublicationSchedule).filter_by(
            publication=publication,
            day=day,
            start=start
        ).first()

        return publication_schedule  # Retourner l'horaire de publication trouvé, ou None si pas trouvé.

    except Exception as e:
        print(f"Erreur lors de la récupération de l'horaire de publication : {str(e)}")
        return None
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def update_publication_schedule(publication: str, day: int, start: str, publication_schedule_dto: PublicationScheduleDTO) -> PublicationSchedule:
    """Met à jour un horaire de publication existant.

    Args:
        publication (str): Le nom de la publication.
        day (int): Le jour de la semaine à mettre à jour.
        start (str): L'heure de début à mettre à jour.
        publication_schedule_dto (PublicationScheduleDTO): Les nouvelles informations d'horaire de publication.

    Returns:
        PublicationSchedule: L'horaire de publication mis à jour.
    """
    session = create_session_local()  # Créer une session locale
    try:
        # Recherche de l'horaire de publication à mettre à jour
        publication_schedule = session.query(PublicationSchedule).filter_by(
            publication=publication,
            day=day,
            start=start
        ).first()

        if not publication_schedule:
            raise ValueError(f"Horaire de publication avec publication {publication}, day {day}, start {start} non trouvé.")

        # Mise à jour des champs
        if publication_schedule_dto.end:
            publication_schedule.end = publication_schedule_dto.end

        # Sauvegarde des modifications
        session.commit()
        session.refresh(publication_schedule)  # Rafraîchir l'objet pour obtenir les valeurs mises à jour

        return publication_schedule  # Retourner l'horaire de publication mis à jour

    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de la mise à jour de l'horaire de publication : {str(e)}")

    finally:
        session.close()  # Assurez-vous de fermer la session à la fin


def delete_publication_schedule(publication: str, day: int, start: str) -> bool:
    """Supprime un horaire de publication de la base de données.

    Args:
        publication (str): Le nom de la publication.
        day (int): Le jour de la semaine de l'horaire à supprimer.
        start (str): L'heure de début de l'horaire à supprimer.

    Returns:
        bool: Retourne True si la suppression est réussie, False sinon.
    """
    session = create_session_local()  # Créer une session locale
    try:
        publication_schedule = session.query(PublicationSchedule).filter_by(
            publication=publication,
            day=day,
            start=start
        ).first()

        if not publication_schedule:
            raise ValueError(f"Horaire de publication avec publication {publication}, day {day}, start {start} non trouvé.")

        session.delete(publication_schedule)
        session.commit()
        return True  # Retourner True si la suppression est réussie
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression de l'horaire de publication : {str(e)}")
        return False
    finally:
        session.close()  # Assurez-vous de fermer la session à la fin
