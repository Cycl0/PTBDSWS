from . import main
from datetime import datetime
from flask import render_template, session, redirect, request, url_for, flash, abort, make_response, current_app
from .. import db
from ..models import Disc
from .forms import DiscplinaForm

@main.route('/', methods=['GET', 'POST'])
def index():
    current_time = datetime.utcnow()
    return render_template(
        'index.html',
        current_time=current_time
    )

@main.route('/disciplinas', methods=['GET', 'POST'])
def CadastroDisciplinas():
    form = DiscplinaForm()
    if form.validate_on_submit():
        try:
            disc = Disc(name=form.name.data, sem=form.sem.data)
            db.session.add(disc)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
    return render_template(
        'disciplinas.html',
        Disc=Disc,
        form=form
    )
