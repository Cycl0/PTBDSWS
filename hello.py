import os
from flask_mail import Mail, Message
from flask import Flask, jsonify, request, make_response, redirect, abort, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
import requests

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'AAAA@@@@3333$$$$'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{os.path.join(basedir, "data.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['FLASKY_ADMIN'] = 'l.cyra@aluno.ifsp.edu.br'


MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

aula = "Aula 10"

def send_message(to, subject, template, **kwargs):
    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        raise ValueError("Mailgun API key or domain is not set.")

    text_body = render_template(template + '.txt', **kwargs)
    html_body = render_template(template + '.html', **kwargs)

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Your Name <mailgun@{MAILGUN_DOMAIN}>",
            "to": to,
            "subject": subject,
            "text": text_body,
            "html": html_body
        }
    )

    # Error handling
    if response.status_code != 200:
        raise Exception(f"Failed to send email: {response.status_code} - {response.text}")

    return response.json()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role', lazy='dynamic')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True, index=True)
    user_last_name = db.Column(db.String(64))
    user_ip = db.Column(db.String(64))
    user_host = db.Column(db.String(64))
    user_inst = db.Column(db.String(64))
    user_disc = db.Column(db.String(64))
    user_role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators = [DataRequired()])
    inst = StringField('Informe a sua Insituição de ensino:', validators = [DataRequired()])
    disc = SelectField('Informe a sua disciplina:', choices = ['DSWA5', 'DWBA4', 'Gestão de Projetos'], validators = [DataRequired()])

    @staticmethod
    def get_role_choices():
        return [(r.name, r.name) for r in Role.query.all()]
    role = SelectField('Informe o seu cargo:', choices=[], validators=[DataRequired()])

    def get_last_name(self):
        if self.name.data:
            parts = self.name.data.split()
            if len(parts) == 1:
                return ""
            else:
                return parts[-1]
        return ""

    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():

    form = NameForm()
    form.role.choices = NameForm.get_role_choices()
    current_time=datetime.utcnow()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.name.data).first()
        if user is None:
            user_data = {
                'user_name': form.name.data,
                'user_last_name': form.get_last_name(),
                'user_ip': request.remote_addr,
                'user_host': request.host_url,
                'user_inst': form.inst.data,
                'user_disc': form.disc.data,
                'user_role_id': Role.query.filter_by(name=form.role.data).first().id
            }

            try:
                user = User(**user_data)
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")

            session['known'] = False
            send_message(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
            send_message('flaskaulasweb@zohomail.com', 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True

        session['name'] = form.name.data
        session['last_name'] = form.get_last_name()
        session['ip'] = request.remote_addr
        session['host'] = request.host_url
        session['inst'] = form.inst.data
        session['disc'] = form.disc.data
        session['role'] = form.role.data

    return render_template('index.html', form=form, current_time=current_time, aula=aula,\
        ip=session.get('ip'),\
        host=session.get('host'),\
        known=session.get('known', False),\
        name=form.name.data,\
        inst=session.get('inst'),\
        disc=session.get('disc'),\
        role=session.get('role'),\
        Role=Role,\
        User=User
    )

@app.route('/user/<name>/<id>/<inst>/')
def user(name, id, inst):
    return render_template('user.html', name=name, id=id, inst=inst, aula=aula)

@app.route('/rotainexistente')
def rotainexistente():
    return render_template('404.html')

@app.route('/contextorequisicao/<name>')
def contextorequisicao(name):
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr
    host = request.host_url
    return render_template('contextorequisicao.html', name=name, user_agent=user_agent, ip=ip, host=host, aula=aula)

@app.route('/codigostatusdiferente')
def codigostatusdiferente():
    abort(400, '400 Bad Request')

@app.route('/objetoresposta')
def objetoresposta():
    answer = '42'
    resp = make_response('''
                            <h1>Avaliação contínua: {}</h1>
                            <h1>This document carries a cookie!</h1>
                            <h2>Cookie value to add: {}</h2>
                            <a href="https://cyclon.pythonanywhere.com/"> Voltar </a>
                         '''.format(aula, answer))
    resp.set_cookie('the_answer_to_everything', answer)
    return resp

@app.route('/redirecionamento')
def redirecionamento():
    return redirect("https://ptb.ifsp.edu.br/", code=302)

@app.route('/abortar')
def abortar():
    abort(404, 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.')

# Tests
def __repr__(self):
    return '<User %r>' % self.username

if __name__ == '__main__':
    app.run(debug=True)
