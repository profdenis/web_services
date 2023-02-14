from flask import render_template, request, jsonify
from . import main
from.. import db
from ..models import Contact, Call


@main.route('/calls')
def all_calls():
    calls = Call.query.all()
    return jsonify(calls)


@main.route('/calls/<int:call_id>')
def call_by_id(call_id):
    call = Call.query.get_or_404(call_id)
    return jsonify(call)
