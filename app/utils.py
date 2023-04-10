from flask import request, current_app


def get_locale():
    print("get_locale was called")
    return 'ru'
    # return request.accept_languages.best_match(['en', 'ru'])
