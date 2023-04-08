from flask import render_template, redirect, url_for, g
from flask_login import current_user
from app.extensions import db
from app.utils import get_locale
from app.queue.forms import FindQueueForm
from app.main import bp


@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
def index():
    form = FindQueueForm()
    if form.validate_on_submit():
        return redirect(url_for('queue.queue', queue_id=form.queue_id.data))
    return render_template('main/index.html', title='Home', find_queue_form=form)


@bp.before_app_request
def before_request():
    if current_user is not None and current_user.is_authenticated:
        db.session.commit()
    g.locale = str(get_locale())


@bp.after_app_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'

    return response
