from app.auth.models import User
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, request
from app.extensions import mail
from flask_mail import Message
from flask_login import current_user


def cur_user_or_temp():
    current_app.logger.info("Cur user: {}".format(current_user))
    if not current_user.is_anonymous:
        return current_user
    temp_user = User()

    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    temp_user.set_ip_address(ip)

    current_app.logger.info("Remote addr: {}".format(request.remote_addr))
    current_app.logger.info("New ip: {}".format(temp_user.ip_address))

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


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)
