from flask import render_template, request, jsonify
from . import main
from.. import db
from ..models import Contact, Call

from flask_jwt_extended import jwt_required, JWTManager


@main.route('/calls')
@jwt_required()
def all_calls():
    calls = Call.query.all()
    return jsonify(calls)


@main.route('/calls/<int:call_id>')
@jwt_required()
def call_by_id(call_id):
    call = Call.query.get_or_404(call_id)
    return jsonify(call)
