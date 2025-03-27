
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services. contact_id_services import (insert_contact_id, get_contact_id, update_contact_id, delete_contact_id)
from dtos.contact_id_dto import ContactIdDTO

contact_id_blueprint = Blueprint('contact_id', __name__)

class ContactIdController:

    @staticmethod
    @contact_id_blueprint.route('/contact', methods=['POST'])
    @jwt_required()
    def create_contact():
        """Créer un nouveau contact"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Données JSON requises'}), 400

            contact_dto = ContactIdDTO(**data)
            new_contact = insert_contact_id(contact_dto)
            return jsonify({'message': 'Contact créé avec succès', 'contact': new_contact.to_dict()}), 201

        except Exception as e:
            return jsonify({'error': 'Erreur lors de la création du contact', 'details': str(e)}), 500

    @staticmethod
    @contact_id_blueprint.route('/contact', methods=['GET'])
    @jwt_required()
    def retrieve_contact():
        """Récupérer un contact par nom et prénom"""
        try:
            lastname = request.args.get('lastname')
            firstname = request.args.get('firstname')

            if not lastname or not firstname:
                return jsonify({'error': 'Nom et prénom sont requis'}), 400

            contact = get_contact_id(lastname, firstname)
            if not contact:
                return jsonify({'error': 'Contact non trouvé'}), 404

            return jsonify(contact.to_dict()), 200

        except Exception as e:
            return jsonify({'error': 'Erreur lors de la récupération du contact', 'details': str(e)}), 500

    @staticmethod
    @contact_id_blueprint.route('/contact', methods=['PUT'])
    @jwt_required()
    def modify_contact():
        """Mettre à jour un contact existant"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Données JSON requises'}), 400

            lastname = data.get('lastname')
            firstname = data.get('firstname')

            if not lastname or not firstname:
                return jsonify({'error': 'Nom et prénom sont requis pour la mise à jour'}), 400

            contact_dto = ContactIdDTO(**data)
            updated_contact = update_contact_id(lastname, firstname, contact_dto)
            return jsonify({'message': 'Contact mis à jour avec succès', 'contact': updated_contact.to_dict()}), 200

        except Exception as e:
            return jsonify({'error': 'Erreur lors de la mise à jour du contact', 'details': str(e)}), 500

    @staticmethod
    @contact_id_blueprint.route('/contact', methods=['DELETE'])
    @jwt_required()
    def remove_contact():
        """Supprimer un contact"""
        try:
            lastname = request.args.get('lastname')
            firstname = request.args.get('firstname')

            if not lastname or not firstname:
                return jsonify({'error': 'Nom et prénom sont requis pour la suppression'}), 400

            success = delete_contact_id(lastname, firstname)
            if not success:
                return jsonify({'error': 'Contact non trouvé ou erreur lors de la suppression'}), 404

            return jsonify({'message': 'Contact supprimé avec succès'}), 200

        except Exception as e:
            return jsonify({'error': 'Erreur lors de la suppression du contact', 'details': str(e)}), 500
