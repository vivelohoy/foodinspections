import sendgrid
import os

DEFAULT_FROM = "Hoy Support <support@vivelohoy.com>"

def send_email(to, _from, subject, body):
    if _from is None:
        _from = DEFAULT_FROM
    sg = sendgrid.SendGridClient(os.environ['SENDGRID_USERNAME'], os.environ['SENDGRID_PASSWORD'])

    message = sendgrid.Mail()
    message.add_to(to)
    message.set_subject(subject)
    message.set_html('<br>'.join(body.split('\n')))
    message.set_text(body)
    message.set_from(_from)

    status, msg = sg.send(message)
    return status, msg