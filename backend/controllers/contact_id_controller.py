
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from .models import ContactId
from .database import engine

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

contact_bp = Blueprint('contacts', __name__)

@contact_bp.route('/', methods=['GET'])
def get_contacts():
    session = Session()
    contacts = session.query(ContactId).all()
    session.close()
    return jsonify([{
        'lastname': c.lastname,
        'firstname': c.firstname
    } for c in contacts])

@contact_bp.route('/<string:lastname>/<string:firstname>', methods=['GET'])
def get_contact(lastname, firstname):
    session = Session()
    contact = session.query(ContactId).filter_by(lastname=lastname, firstname=firstname).first()
    session.close()
    if contact:
        return jsonify({
            'lastname': contact.lastname,
            'firstname': contact.firstname
        })
    return jsonify({'message': 'Contact not found'}), 404

@contact_bp.route('/', methods=['POST'])
def create_contact():
    data = request.json
    session = Session()
    try:
        new_contact = ContactId(
            lastname=data['lastname'],
            firstname=data['firstname']
        )
        session.add(new_contact)
        session.commit()
        return jsonify({'message': 'Contact created'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@contact_bp.route('/<string:lastname>/<string:firstname>', methods=['DELETE'])
def delete_contact(lastname, firstname):
    session = Session()
    contact = session.query(ContactId).filter_by(lastname=lastname, firstname=firstname).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    session.delete(contact)
    session.commit()
    session.close()
    return jsonify({'message': 'Contact deleted'})

# Pour intégrer ce Blueprint dans app.py :
# from .routes_contact import contact_bp
# app.register_blueprint(contact_bp, url_prefix='/contacts')
