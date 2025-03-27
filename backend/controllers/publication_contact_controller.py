from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.publication_contact_service import (insert_publication_contact,
                                                  get_publication_contact,
                                                  update_publication_contact,
                                                  delete_publication_contact)
from dtos.publication_contact_dto import PublicationContactDTO  # Assuming you have a DTO for this
from datetime import datetime

# Création du blueprint 'publication_contact'
publication_contact_blueprint = Blueprint('publication_contact', __name__)


class PublicationContactController:

    @staticmethod
    @publication_contact_blueprint.route('', methods=['POST'])
    @jwt_required()  # Protéger la route avec l'authentification JWT
    def create_publication_contact():
        try:
            # Récupérer les données de la requête JSON
            data = request.get_json()
            if not data:
                return jsonify({'error':
                                'Invalid request, JSON required'}), 400

            # Créer un DTO avec les données
            publication_contact_dto = PublicationContactDTO(**data)

            # Appeler le service pour insérer dans la base de données
            publication_contact = insert_publication_contact(
                publication_contact_dto)

            return jsonify({
                'message': 'Publication contact created successfully',
                'publication_contact': publication_contact.to_dict()
            }), 201

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    @staticmethod
    @publication_contact_blueprint.route(
        '/<string:publication>/<string:lastname>/<string:firstname>',
        methods=['GET'])
    @jwt_required()
    def get_publication_contact_by_id(publication, lastname, firstname):
        try:
            # Récupérer les informations de la publication à partir des paramètres
            publication_contact = get_publication_contact(
                publication, lastname, firstname)

            if not publication_contact:
                return jsonify({'error': 'PublicationContact not found'}), 404

            return jsonify(
                {'publication_contact': publication_contact.to_dict()}), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    @staticmethod
    @publication_contact_blueprint.route(
        '/<string:publication>/<string:lastname>/<string:firstname>',
        methods=['PUT'])
    @jwt_required()
    def update_publication_contact(publication, lastname, firstname):
        try:
            # Récupérer les données de la requête JSON
            data = request.get_json()
            if not data:
                return jsonify({'error':
                                'Invalid request, JSON required'}), 400

            # Créer un DTO avec les nouvelles données
            publication_contact_dto = PublicationContactDTO(**data)

            # Appeler le service pour mettre à jour la publication dans la base de données
            updated_publication_contact = update_publication_contact(
                publication, lastname, firstname, publication_contact_dto)

            return jsonify({
                'message':
                'Publication contact updated successfully',
                'publication_contact':
                updated_publication_contact.to_dict()
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500

    @staticmethod
    @publication_contact_blueprint.route(
        '/<string:publication>/<string:lastname>/<string:firstname>',
        methods=['DELETE'])
    @jwt_required()
    def delete_publication_contact(publication, lastname, firstname):
        try:
            # Appeler le service pour supprimer la publication dans la base de données
            success = delete_publication_contact(publication, lastname,
                                                 firstname)

            if not success:
                return jsonify({'error': 'PublicationContact not found'}), 404

            return jsonify(
                {'message': 'Publication contact deleted successfully'}), 200

        except Exception as e:
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e)
            }), 500
