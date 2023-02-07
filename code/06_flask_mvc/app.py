import json

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import jsonpickle

app = Flask(__name__)
app.secret_key = 'allo'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///contacts.sqlite'
db = SQLAlchemy(app)

from models import Contact, Call, ContactEncoder

app.json_encoder = ContactEncoder


@app.route('/contacts')
def all_contacts():
    contacts = Contact.query.all()
    # return json.loads(jsonpickle.encode(contacts))
    return jsonify(contacts)


@app.route('/contacts/<int:contact_id>')
def contact_by_id(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify(contact)


@app.route('/calls')
def all_calls():
    calls = Call.query.all()
    # return json.loads(jsonpickle.encode(calls))
    return jsonify(calls)


@app.route('/calls/<int:call_id>')
def call_by_id(call_id):
    call = Call.query.get_or_404(call_id)
    return jsonify(call)


@app.errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden', 'code': 403})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found', 'code': 404})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error', 'code': 500})
        response.status_code = 500
        return response
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
