from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

from . import views, views_contacts, views_calls
from ..models import ContactEncoder

main.json_encoder = ContactEncoder
