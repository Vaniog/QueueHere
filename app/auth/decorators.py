from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def check_is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_confirmed:
            flash("Please confirm your account!", "warning")
            return redirect(url_for("auth.inactive"))
        return func(*args, **kwargs)

    return decorated_function
