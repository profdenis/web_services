from flask import request, jsonify, abort
from . import main
from .. import db
from ..models import Contact


@main.route('/contacts')
def all_contacts():
    contacts = Contact.query.all()
    return jsonify({'success': True, 'data': contacts})


@main.route('/contacts/<int:contact_id>')
def contact_by_id(contact_id: int):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify({'success': True, 'data': contact})


@main.route('/contacts/<int:contact_id>/calls')
def calls_of_contact_by_id(contact_id: int):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify({'success': True, 'data': contact.calls})


@main.route('/contacts', methods=['POST'])
def new_contact():
    data = request.json
    name = data.get('name', None)
    if not name:
        return {'success': False,
                'error': 'Missing Name',
                'code': 409}, 409
    address = data.get('address', None)
    email = data.get('email', None)
    phone = data.get('phone', None)

    contact = Contact(address=address, email=email, name=name, phone=phone)
    db.session.add(contact)
    db.session.commit()
    return jsonify({'success': True, 'data': contact})


@main.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)

    data = request.json
    contact.name = data.get('name', contact.name)
    if not contact.name:
        return {'success': False,
                'error': 'Missing Name',
                'code': 409}, 409
    contact.address = data.get('address', contact.address)
    contact.email = data.get('email', contact.email)
    contact.phone = data.get('phone', contact.phone)

    db.session.add(contact)
    db.session.commit()
    return jsonify({'success': True, 'data': contact})


@main.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    result = db.session.execute(db.delete(Contact).where(Contact.contact_id == contact_id))
    db.session.commit()
    if result.rowcount == 1:
        return jsonify({'success': True, 'data': f'Contact {contact_id} deleted'})
    else:
        abort(404)
