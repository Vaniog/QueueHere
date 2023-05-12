from flask import render_template, redirect, url_for
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return redirect(url_for('main.index'))


@bp.app_errorhandler(500)
def internal_error(error):
    return redirect(url_for('main.index'))
