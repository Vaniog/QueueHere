from flask import request, current_app


def get_locale():
    language = request.accept_languages.best_match(current_app.config['LANGUAGES'])
    print('Accept-Language:', request.accept_languages)
    print('Guessed language:', language)
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'ru'
