from flask import Flask, request, make_response, redirect, abort
app = Flask(__name__)

aula = "Aula 030"

@app.route('/')
def index():
    return '''
            <h1>Avaliação contínua: {}</h1>
            <ul>
                <li><a href="https://cyclon.pythonanywhere.com/"> Home </a></li>
                <li><a href="https://cyclon.pythonanywhere.com/user/Lucas%20Kenzo%20Cyra/PT3025764/IFSP"> Identificação </a></li>
                <li><a href="https://cyclon.pythonanywhere.com/contextorequisicao"> Contexto da requisição </a></li>
            </ul>
           '''.format(aula)

@app.route('/user/<name>/<id>/<instution>')
def user(name, id, instution):
    return '''
            <h1>Avaliação contínua: {}</h1>
            <h2>Aluno: {}</h2>
            <h2>Prontuário: {}</h2>
            <h2>Instituição: {}</h2>
            <a href="https://cyclon.pythonanywhere.com/"> Voltar </a>
           '''.format(aula, name, id, instution)

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
