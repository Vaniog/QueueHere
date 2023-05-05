from app.auth.models import User
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, request, render_template
from app.extensions import mail
from flask_mail import Message
from flask_login import current_user
from flask_babel import _
import threading


def cur_user_or_temp():
    if not current_user.is_anonymous:
        return current_user
    temp_user = User()

    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    ip += request.headers.get('User-Agent')

    temp_user.set_ip_address(ip)

    maybe_user = User.query.filter_by(ip_address=temp_user.ip_address).first()

    if maybe_user is not None:
        temp_user = maybe_user
    else:
        temp_user.username = temp_user.ip_address
        temp_user.email = temp_user.ip_address
        temp_user.is_guest = True
        temp_user.name_to_print = ""

    return temp_user


def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False


class SendEmailThread(threading.Thread):
    def __init__(self, app, msg):
        self.current_app = app
        self.msg = msg
        threading.Thread.__init__(self)
        self.daemon = True

    UPDATE_FREQUENCY = 2  # in seconds

    def run(self):
        with self.current_app.app_context():
            mail.send(self.msg)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )

    SendEmailThread(current_app._get_current_object(), msg).start()


def send_password_reset_email(user):
    token = user.generate_reset_password_token()
    send_email(subject=_(_('[QueueHere] Reset Your Password')),
               to=user.email,
               template=render_template('auth/email/reset_password.html',
                                        user=user, token=token))
