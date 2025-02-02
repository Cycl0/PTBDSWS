from flask import render_template
from . import main
from datetime import datetime

@main.app_errorhandler(404)
def page_not_found(e):
    current_time = datetime.utcnow()
    return render_template('404.html', current_time=current_time), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
