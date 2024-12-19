from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired
from flask import current_app

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    inst = StringField('Informe a sua Instituição de ensino:', validators=[DataRequired()])
    disc = SelectField('Informe a sua disciplina:', choices=['DSWA5', 'DWBA4', 'Gestão de Projetos'], validators=[DataRequired()])

    @staticmethod
    def get_role_choices():
        return [(r.name, r.name) for r in Role.query.all()]

    role = SelectField('Informe o seu cargo:', choices=[], validators=[DataRequired()])

    send_email_admin_1 = BooleanField('Deseja enviar e-mail para admin 1?')
    send_email_admin_2 = BooleanField('Deseja enviar e-mail para admin 2?')

    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        self.send_email_admin_1.label.text = f'Deseja enviar e-mail para {current_app.config["FLASKY_ADMIN_1"]}'
        self.send_email_admin_2.label.text = f'Deseja enviar e-mail para {current_app.config["FLASKY_ADMIN_2"]}'

    def get_last_name(self):
        if self.name.data:
            parts = self.name.data.split()
            if len(parts) == 1:
                return ""
            else:
                return parts[-1]
        return ""

    submit = SubmitField('Submit')
