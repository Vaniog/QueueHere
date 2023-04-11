from flask import request, current_app


def get_locale():
    return request.accept_languages.best_match(['en', 'ru'])
