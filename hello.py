from flask import Flask, request, make_response, redirect, abort, render_template
from flask_bootstrap import Bootstrap
#from flask_moment import moment
from datetime import datetime, timedelta

app = Flask(__name__)
bootstrap = Bootstrap(app)

aula = "Aula 030"

@app.route('/')
def index():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%B %d, %Y %I:%M %p")
    minutes_ago = (datetime.now() - current_time).seconds // 60
    return render_template('index.html', current_time=formatted_time, minutes_ago=minutes_ago)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/rotainexistente')
def rotainexistente():
    return render_template('404.html')


@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent')
    ip_remote = request.remote_addr
    host = request.host_url
    return '''
              <h1>Avaliação contínua: {}</h1>
              <h2>Seu navegador é: {}</h2>
              <h2>O IP do cumputador remoto é: {}</h2>
              <h2>O host da aplicação é: {}</h2>
              <a href="https://cyclon.pythonanywhere.com/"> Voltar </a>
           '''.format(aula, user_agent, ip_remote, host)

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
