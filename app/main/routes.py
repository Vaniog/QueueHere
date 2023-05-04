from flask import render_template, redirect, url_for, current_app, request, session
from flask_login import current_user
from app.extensions import db, babel
from app.queue.forms import FindQueueForm
from app.main import bp
from app.main.models import Stats, StatsEnum
from flask_login import login_required
from app.auth.decorators import check_is_confirmed


@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
def index():
    form = FindQueueForm()
    if form.validate_on_submit():
        return redirect(url_for('queue.queue', queue_id=form.queue_id.data))
    return render_template('main/index.html', find_queue_form=form)


@bp.route('/give_like', methods=['POST'])
@login_required
@check_is_confirmed
def give_like():
    if not current_user.like_given:
        current_user.like_given = True
        Stats.increase(StatsEnum.likes_given)
        db.session.commit()

    return {"likes_amount": Stats.get_count_of(StatsEnum.likes_given)}, 200


@bp.before_app_request
def before_request():
    if current_user is not None and current_user.is_authenticated:
        db.session.commit()


@bp.after_app_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.cache_control.public = True
    response.cache_control.max_age = 0
    session.permanent = True

    return response
