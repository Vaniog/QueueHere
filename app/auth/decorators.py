from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def check_is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_confirmed:
            flash("Please confirm your account!", "warning")
            return redirect(url_for("auth.inactive"))
        return func(*args, **kwargs)

    return decorated_function


def check_is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(404)
        return func(*args, **kwargs)

    return decorated_function
