from flask import render_template, session, redirect, url_for, request, abort, make_response, current_app
from .. import db
from ..models import User, Role
from ..email import send_message
from . import main
from .forms import NameForm
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    current_time = datetime.utcnow()

    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.name.data).first()
        if user is None:
            role = Role.query.filter_by(name=form.role.data).first()
            user_data = {
                'user_name': form.name.data,
                'user_last_name': form.get_last_name(),
                'user_ip': request.remote_addr,
                'user_host': request.host_url,
                'user_inst': form.inst.data,
                'user_disc': form.disc.data,
                'user_role_id': role.id if role else None
            }

            try:
                user = User(**user_data)
                db.session.add(user)
                db.session.commit()
                session['known'] = False
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")
                session['known'] = False

            if form.send_email_admin_1.data:
                send_message(
                    current_app.config.get('FLASKY_ADMIN_1'),
                    'New User',
                    'mail/new_user',
                    user=user
                )

            if form.send_email_admin_2.data:
                send_message(
                    current_app.config.get('FLASKY_ADMIN_2'),
                    'New User',
                    'mail/new_user',
                    user=user
                )
            if form.send_email_user.data is not "":
                send_message(
                    form.send_email_user.data,
                    'New User',
                    'mail/new_user',
                    user=user
                )
        else:
            session['known'] = True

        session.update({
            'name': form.name.data,
            'last_name': form.get_last_name(),
            'ip': request.remote_addr,
            'host': request.host_url,
            'inst': form.inst.data,
            'disc': form.disc.data,
            'role': form.role.data
        })

    return render_template(
        'index.html',
        form=form,
        current_time=current_time,
        aula=current_app.config.get('AULA'),
        ip=session.get('ip'),
        host=session.get('host'),
        known=session.get('known', False),
        name=session.get('name'),
        inst=session.get('inst'),
        disc=session.get('disc'),
        role=session.get('role'),
        Role=Role,
        User=User
    )


@main.route('/user/<name>/<id>/<inst>/')
def user(name, id, inst):
    return render_template(
        'user.html',
        name=name,
        id=id,
        inst=inst,
        aula=current_app.config.get('AULA')
    )


@main.route('/rotainexistente')
def rotainexistente():
    return render_template('404.html'), 404


@main.route('/contextorequisicao/<name>')
def contextorequisicao(name):
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr
    host = request.host_url
    return render_template(
        'contextorequisicao.html',
        name=name,
        user_agent=user_agent,
        ip=ip,
        host=host,
        aula=current_app.config.get('AULA')
    )


@main.route('/codigostatusdiferente')
def codigostatusdiferente():
    abort(400, '400 Bad Request')


@main.route('/objetoresposta')
def objetoresposta():
    answer = '42'
    resp = make_response(f'''
        <h1>Avaliação contínua: {current_app.config.get("AULA", "N/A")}</h1>
        <h1>This document carries a cookie!</h1>
        <h2>Cookie value to add: {answer}</h2>
        <a href="https://cyclon.pythonanywhere.com/"> Voltar </a>
    ''')
    resp.set_cookie('the_answer_to_everything', answer)
    return resp


@main.route('/redirecionamento')
def redirecionamento():
    return redirect("https://ptb.ifsp.edu.br/", code=302)


@main.route('/abortar')
def abortar():
    abort(404, 'The requested URL was not found on the server. If you entered the URL manually, please check your spelling and try again.')
