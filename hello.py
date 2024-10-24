from flask import Flask, request, make_response, redirect, abort, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

aula = "Aula 030"

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>/<id>/<inst>/')
def user(name, id, inst):
    return render_template('user.html', name=name, id=id, inst=inst)

@app.route('/rotainexistente')
def rotainexistente():
    return render_template('404.html')

@app.route('/contextorequisicao/<name>')
def contextorequisicao(name):
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr
    host = request.host_url
    return render_template('contextorequisicao.html', name=name, user_agent=user_agent, ip=ip, host=host)

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
