from flask import render_template, request, jsonify
from . import main
from ..models import Contact, Call


@main.errorhandler(Exception)
def error_handler(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'success': False, 'error': error.name, 'code': error.code})
        response.status_code = error.code
        return response
    return render_template('error.html', error=error), error.code
