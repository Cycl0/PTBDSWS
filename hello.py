from flask import Flask, request, make_response, redirect, abort
app = Flask(__name__)

@app.route('/')
def index():
    return '''
            <h1>Hello World!</h1>
            <p>Lucas Kenzo Cyra</p>
            <p>PT3025764</p>
           '''

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent')
    return '''
              <h1>Your browser is</h1>
              <p>{}</p>
           '''.format(user_agent)

@app.route('/codigostatusdiferente')
def codigostatusdiferente():
    abort(400, '400 Bad Request')

@app.route('/objetoresposta')
def objetoresposta():
    answer = '42'
    resp = make_response('''
                            <h1>This document carries a cookie!</h1>
                            <p>Cookie value to add: {}</p>
                         '''.format(answer))
    resp.set_cookie('the_answer_to_everything', answer)
    return resp

@app.route('/redirecionamento')
def redirecionamento():
    return redirect("https://ptb.ifsp.edu.br/", code=302)

@app.route('/abortar')
def abortar():
    abort(404, 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.')
