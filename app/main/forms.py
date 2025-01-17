from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask import current_app
from ..models import Disc



class DiscplinaForm(FlaskForm):
    name = StringField('Cadastre a nova disciplina e o semestre associado:', validators=[DataRequired()])

    sem = RadioField(choices=['1º semestre', '2º semestre', '3º semestre', '4º semestre', '5º semestre', '6º semestre'], validators=[DataRequired()])

    submit = SubmitField('Cadastrar')
