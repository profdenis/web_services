from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

from . import views
from ..models import ContactEncoder

main.json_encoder = ContactEncoder
