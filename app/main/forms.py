from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask import current_app
from ..models import Role, User


'''
class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[ DataRequired(), Length(min=8, message='Senha deve ter no minimo 8 characteres') ])
    inst = StringField('Informe a sua Instituição de ensino:', validators=[DataRequired()])
    disc = SelectField('Informe a sua disciplina:', choices=['DSWA5', 'DWBA4', 'Gestão de Projetos'], validators=[DataRequired()])

    @staticmethod
    def get_role_choices():
        return [(r.name, r.name) for r in Role.query.all()]

    role = SelectField('Informe o seu cargo:', choices=[], validators=[DataRequired()])

    send_email_user = StringField('*Apenas para recipientes autorizados* - Qual é o seu email (Envio de notificação do novo usuário)?', validators=[Email(message="Por favor insira um email válido")])

    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        self.role.choices = self.get_role_choices()
        self.send_email_admin_1.label.text = f'Deseja enviar e-mail para {current_app.config["FLASKY_ADMIN_1"]}'
        self.send_email_admin_2.label.text = f'Deseja enviar e-mail para {current_app.config["FLASKY_ADMIN_2"]}'

    send_email_admin_1 = BooleanField('Deseja enviar e-mail para admin 1?')
    send_email_admin_2 = BooleanField('Deseja enviar e-mail para admin 2?')

    def get_last_name(self):
        if self.name.data:
            parts = self.name.data.split()
            if len(parts) == 1:
                return ""
            else:
                return parts[-1]
        return ""

    submit = SubmitField('Submit')
'''

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    inst = StringField('Informe a sua Instituição de ensino:', validators=[DataRequired()])
    disc = SelectField('Informe a sua disciplina:', choices=['DSWA5', 'DWBA4', 'Gestão de Projetos'], validators=[DataRequired()])

    @staticmethod
    def get_role_choices():
        return [(r.name, r.name) for r in Role.query.all()]

    role = SelectField('Informe o seu cargo:', choices=[], validators=[DataRequired()])

    send_email_user = StringField('*Apenas para recipientes autorizados* - Qual é o seu email (Envio de notificação do novo usuário)?', validators=[Email(message="Por favor insira um email válido")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = self.get_role_choices()
        self.send_email_admin_1.label.text = f'Deseja enviar e-mail para {current_app.config["FLASKY_ADMIN_1"]}'
        self.send_email_admin_2.label.text = f'Deseja enviar e-mail para {current_app.config["FLASKY_ADMIN_2"]}'

    send_email_admin_1 = BooleanField('Deseja enviar e-mail para admin 1?')
    send_email_admin_2 = BooleanField('Deseja enviar e-mail para admin 2?')
    submit = SubmitField('Register')

    def get_last_name(self):
        if self.name.data:
            parts = self.name.data.split()
            if len(parts) == 1:
                return ""
            else:
                return parts[-1]
        return ""
    def validate_email(self, field):
        if User.query.filter_by(user_email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(user_name=field.data.lower()).first():
            raise ValidationError('Username already in use.')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data.lower()).first():
            raise ValidationError('Name already registered.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
