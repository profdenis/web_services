from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'allo'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///contacts3.sqlite'
db = SQLAlchemy(app)

from models import Contact, Call, ContactEncoder

app.json_encoder = ContactEncoder


@app.route('/contacts')
def all_contacts():
    contacts = Contact.query.all()
    return jsonify({'success': True, 'data': contacts})


@app.route('/contacts/<int:contact_id>')
def contact_by_id(contact_id: int):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify({'success': True, 'data': contact})


@app.route('/contacts', methods=['POST'])
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


@app.route('/contacts/<int:contact_id>', methods=['PUT'])
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


@app.route('/calls')
def all_calls():
    calls = Call.query.all()
    return jsonify(calls)


@app.route('/calls/<int:call_id>')
def call_by_id(call_id):
    call = Call.query.get_or_404(call_id)
    return jsonify(call)


@app.errorhandler(Exception)
def error_handler(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'success': False, 'error': error.name, 'code': error.code})
        response.status_code = error.code
        return response
    return render_template('error.html', error=error), error.code


if __name__ == '__main__':
    app.run()
