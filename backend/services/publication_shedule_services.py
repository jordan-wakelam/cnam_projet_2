
from sqlalchemy.orm import Session
from models import create_session_local  # Assure-toi que cette fonction existe pour créer une session SQLAlchemy
from models.publication_schedule_model import PublicationSchedule
from typing import List, Optional
from datetime import time


def insert_publication_schedule(publication: str, day: int, start: time, end: Optional[time] = None) -> PublicationSchedule:
    """Insère une nouvelle planification de publication dans la base de données.
    
    Args:
        publication (str): Le nom de la publication.
        day (int): Le jour de la semaine (1 pour lundi, 7 pour dimanche).
        start (time): L'heure de début de la publication.
        end (Optional[time]): L'heure de fin de la publication (optionnel).
    
    Returns:
        PublicationSchedule: L'objet PublicationSchedule inséré.
    """
    session = create_session_local()
    try:
        # Créer un nouvel objet PublicationSchedule
        new_schedule = PublicationSchedule(
            publication=publication,
            day=day,
            start=start,
            end=end
        )
        
        # Ajouter et valider la transaction
        session.add(new_schedule)
        session.commit()
        session.refresh(new_schedule)  # Rafraîchir pour obtenir les valeurs après insertion
        return new_schedule
    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de l'insertion de la planification : {str(e)}")
    finally:
        session.close()


def get_publication_schedule(publication: str, day: int, start: time) -> Optional[PublicationSchedule]:
    """Récupère une planification de publication à partir de la base de données.
    
    Args:
        publication (str): Le nom de la publication.
        day (int): Le jour de la semaine de la publication.
        start (time): L'heure de début de la publication.
    
    Returns:
        Optional[PublicationSchedule]: L'objet PublicationSchedule trouvé, ou None si non trouvé.
    """
    session = create_session_local()
    try:
        # Rechercher une planification de publication par publication, jour et heure de début
        schedule = session.query(PublicationSchedule).filter_by(
            publication=publication,
            day=day,
            start=start
        ).first()

        return schedule
    except Exception as e:
        print(f"Erreur lors de la récupération de la planification : {str(e)}")
        return None
    finally:
        session.close()


def get_all_publication_schedules() -> List[PublicationSchedule]:
    """Récupère toutes les planifications de publication dans la base de données.
    
    Returns:
        List[PublicationSchedule]: Liste de toutes les planifications de publication.
    """
    session = create_session_local()
    try:
        schedules = session.query(PublicationSchedule).all()
        return schedules
    except Exception as e:
        print(f"Erreur lors de la récupération des planifications : {str(e)}")
        return []
    finally:
        session.close()


def update_publication_schedule(publication: str, day: int, start: time, end: Optional[time]) -> PublicationSchedule:
    """Met à jour une planification de publication dans la base de données.
    
    Args:
        publication (str): Le nom de la publication.
        day (int): Le jour de la semaine de la publication.
        start (time): L'heure de début de la publication.
        end (Optional[time]): La nouvelle heure de fin de la publication (optionnel).
    
    Returns:
        PublicationSchedule: L'objet PublicationSchedule mis à jour.
    """
    session = create_session_local()
    try:
        # Rechercher la planification de publication existante
        schedule = session.query(PublicationSchedule).filter_by(
            publication=publication,
            day=day,
            start=start
        ).first()

        if not schedule:
            raise ValueError("La planification demandée n'existe pas.")

        # Mise à jour des informations de la planification
        if end is not None:
            schedule.end = end

        # Sauvegarder les modifications
        session.commit()
        session.refresh(schedule)
        return schedule
    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de la mise à jour de la planification : {str(e)}")
    finally:
        session.close()


def delete_publication_schedule(publication: str, day: int, start: time) -> bool:
    """Supprime une planification de publication de la base de données.
    
    Args:
        publication (str): Le nom de la publication.
        day (int): Le jour de la semaine de la publication.
        start (time): L'heure de début de la publication.
    
    Returns:
        bool: True si la planification a été supprimée avec succès, False sinon.
    """
    session = create_session_local()
    try:
        # Rechercher la planification à supprimer
        schedule = session.query(PublicationSchedule).filter_by(
            publication=publication,
            day=day,
            start=start
        ).first()

        if not schedule:
            raise ValueError("La planification demandée n'existe pas.")

        # Supprimer la planification
        session.delete(schedule)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression de la planification : {str(e)}")
        return False
    finally:
        session.close()
