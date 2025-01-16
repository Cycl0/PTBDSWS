from . import main
from datetime import datetime
from flask import render_template, session, redirect, request, url_for, flash, abort, make_response, current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from .. import db
from ..models import User, Role
from ..email import send_email, send_message
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

@main.route('/', methods=['GET', 'POST'])
def index():
    current_time = datetime.utcnow()

    return render_template(
        'index.html',
        current_time=current_time,
        aula=current_app.config.get('AULA'),
        ip=current_user.user_ip if current_user.is_authenticated else None,
        host=current_user.user_host if current_user.is_authenticated else None,
        known=True if current_user.is_authenticated else False,
        name=current_user.name if current_user.is_authenticated else None,
        user_name=current_user.user_name if current_user.is_authenticated else None,
        inst=current_user.user_inst if current_user.is_authenticated else None,
        disc=current_user.user_disc if current_user.is_authenticated else None,
        role=current_user.role.name if current_user.is_authenticated and current_user.role else None,
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

'''
@main.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.user_confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('main.unconfirmed'))
'''

@main.route('/auth/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.user_confirmed:
        return redirect(url_for('main.index'))
    return render_template('/auth/unconfirmed.html')


@main.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('/auth/login.html', form=form)


@main.route('/auth/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/auth/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name=form.role.data).first()
        user_data = {
            'user_email': form.email.data.lower(),
            'name': form.name.data,
            'user_name': form.username.data,
            'password': form.password.data,
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
        if form.send_email_user.data != "":
            send_message(
                form.send_email_user.data,
                'New User',
                'mail/new_user',
                user=user
            )
        token = user.generate_confirmation_token()
        send_email(user.user_email, 'Confirm Your Account',
                   '/auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        flash('<p>To confirm your account <a href="' + url_for('main.confirm', token=token, _external=True) + '">click here</a></p>')
        return redirect(url_for('main.login'))
    return render_template('/auth/register.html', form=form)


@main.route('/auth/confirm/<token>')
@login_required
def confirm(token):
    if current_user.user_confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@main.route('/auth/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               '/auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    flash('<p>To confirm your account <a href="' + url_for('main.confirm', token=token, _external=True) + '">click here</a></p>')
    return redirect(url_for('main.index'))


@main.route('/auth/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@main.route('/auth/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.user_email, 'Reset Your Password',
                       '/auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        flash('<p>To reset your password <a href="' + url_for('main.password_reset', token=token, _external=True) + '">click here</a></p>')
        return redirect(url_for('main.login'))
    return render_template('/auth/reset_password.html', form=form)


@main.route('/auth/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('/auth/reset_password.html', form=form)


@main.route('/auth/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       '/auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            flash('<p>To confirm your new email address <a href="' + url_for('main.change_email', token=token, _external=True) + '">click here</a></p>')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@main.route('/auth/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))