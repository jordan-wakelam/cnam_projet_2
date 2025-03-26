from flask import Flask, request, jsonify, Blueprint
from sqlalchemy.orm import sessionmaker
from .models import PublicationContact, 
from .database import engine

app = Flask(__name__)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

publication_bp = Blueprint('publication_contacts', __name__)

@publication_bp.route('/', methods=['GET'])
def get_publication_contacts():
    session = Session()
    contacts = session.query(PublicationContact).all()
    session.close()
    return jsonify([{
        'publication': c.publication,
        'lastname': c.lastname,
        'firstname': c.firstname,
        'type': c.type,
        'value': c.value,
        'id': c.id
    } for c in contacts])

@publication_bp.route('/<string:publication>/<string:lastname>/<string:firstname>', methods=['GET'])
def get_publication_contact(publication, lastname, firstname):
    session = Session()
    contact = session.query(PublicationContact).filter_by(
        publication=publication, lastname=lastname, firstname=firstname
    ).first()
    session.close()
    if contact:
        return jsonify({
            'publication': contact.publication,
            'lastname': contact.lastname,
            'firstname': contact.firstname,
            'type': contact.type,
            'value': contact.value,
            'id': contact.id
        })
    return jsonify({'message': 'Contact not found'}), 404

@publication_bp.route('/', methods=['POST'])
def create_publication_contact():
    data = request.json
    session = Session()
    try:
        new_contact = PublicationContact(
            publication=data['publication'],
            lastname=data['lastname'],
            firstname=data['firstname'],
            type=data['type'],
            value=data['value'],
            id=data['id']
        )
        session.add(new_contact)
        session.commit()
        return jsonify({'message': 'Contact created'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@publication_bp.route('/<string:publication>/<string:lastname>/<string:firstname>', methods=['PUT'])
def update_publication_contact(publication, lastname, firstname):
    session = Session()
    contact = session.query(PublicationContact).filter_by(
        publication=publication, lastname=lastname, firstname=firstname
    ).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    data = request.json
    contact.type = data.get('type', contact.type)
    contact.value = data.get('value', contact.value)
    session.commit()
    session.close()
    return jsonify({'message': 'Contact updated'})

@publication_bp.route('/<string:publication>/<string:lastname>/<string:firstname>', methods=['DELETE'])
def delete_publication_contact(publication, lastname, firstname):
    session = Session()
    contact = session.query(PublicationContact).filter_by(
        publication=publication, lastname=lastname, firstname=firstname
    ).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    session.delete(contact)
    session.commit()
    session.close()
    return jsonify({'message': 'Contact deleted'})

app.register_blueprint(publication_bp, url_prefix='/publication_contacts')

if __name__ == '__main__':
    app.run(debug=True)
