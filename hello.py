from flask import Flask, request, make_response, redirect, abort, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'AAAA@@@@3333$$$$'

aula = "Aula 060"

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators = [DataRequired()])
    last_name = StringField('Informe o seu sobrenome:', validators = [DataRequired()])
    inst = StringField('Informe a sua Insituição de ensino:', validators = [DataRequired()])
    disc = SelectField('Informe a sua disciplina:', choices = ['DSWA5', 'DWBA4', 'Gestão de Projetos'], validators = [DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    current_time=datetime.utcnow()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you havee changed your name!')

        session['ip'] = request.remote_addr
        session['host'] = request.host_url

        session['name'] = form.name.data
        session['last_name'] = form.last_name.data
        session['inst'] = form.inst.data
        session['disc'] = form.disc.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, ip=session.get('ip'), host=session.get('host'), name=session.get('name'), last_name=session.get('last_name'), inst=session.get('inst'), disc=session.get('disc'), current_time=current_time, aula=aula)

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

if __name__ == '__main__':
    app.run(debug=True)
