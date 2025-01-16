from flask import current_app, render_template
from . import mail
import requests
from datetime import datetime
from flask_mail import Message
from threading import Thread

def send_message(to, subject, template, **kwargs):
    app = current_app

    if not app.config['MAILGUN_API_KEY'] or not app.config['MAILGUN_DOMAIN']:
        raise ValueError("Mailgun API key or domain is not set.")

    text_body = render_template(template + '.txt', **kwargs)
    html_body = render_template(template + '.html', **kwargs)

    response = requests.post(
        f"https://api.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages",
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={
            "from": f"Your Name <mailgun@{app.config['MAILGUN_DOMAIN']}>",
            "to": to,
            "subject": subject,
            "text": text_body,
            "html": html_body
        }
    )

    if response.status_code != 200:
        raise Exception(f"Failed to send email: {response.status_code} - {response.text}")

    return response.json()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email_zoho(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    #print('text: ' + "Novo usuário cadastrado: " + newUser, flush=True)

    resposta = requests.post(
        f"https://api.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages",
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={
        "from": f"Your Name <mailgun@{app.config['MAILGUN_DOMAIN']}>",
                "to": to,
                "subject": subject,
                "html": render_template(template + '.html', **kwargs)
        }
    )
