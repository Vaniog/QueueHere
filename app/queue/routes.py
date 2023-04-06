from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app.queue.models import Queue
from app.auth.utils import cur_user_or_temp
from app.auth.decorators import check_is_confirmed
from app.extensions import db
from app.queue.forms import CreateQueueForm, JoinQueueForm, KillQueueForm, ForgetQueueForm
from app.queue import bp
from werkzeug.urls import url_parse


@bp.route('/queue/<queue_id>', methods=['GET', 'POST'])
def queue(queue_id):
    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()
    join_form = JoinQueueForm()

    cur_user = cur_user_or_temp(request)

    if join_form.validate_on_submit():
        if cur_queue.contains(cur_user):
            flash('You have already enter this queue.', 'danger')
            return redirect(url_for('queue.queue', queue_id=queue_id))

        cur_queue.add_member(cur_user, join_form.name_to_print.data)
        cur_user.name_to_print = join_form.name_to_print.data
        db.session.commit()
        return redirect(url_for('queue.queue', queue_id=queue_id))

    return render_template('queue/queue.html',
                           queue=cur_queue,
                           join_queue_form=join_form,
                           watching_user=cur_user)


@bp.route('/create_queue', methods=['GET', 'POST'])
@login_required
@check_is_confirmed
def create_queue():
    form = CreateQueueForm()
    if form.validate_on_submit():
        max_queues = current_app.config['MAX_OWNED_QUEUES_PER_USER']
        if len(current_user.owned_queues) >= max_queues:
            flash('You cant create more than ' +
                  str(max_queues) + ' queues', 'danger')
            return redirect(url_for('queue.create_queue'))

        new_queue = Queue(name=form.name.data, admin=current_user)

        db.session.add(new_queue)
        db.session.commit()

        return redirect(url_for('queue.queue', queue_id=new_queue.id))
    return render_template('queue/create_queue.html', create_queue_form=form, title='Create Queue')


@bp.route('/leave_queue/<queue_id>')
def leave_queue(queue_id):
    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()

    cur_queue.leave_member(cur_user_or_temp(request))

    db.session.commit()
    return redirect(url_for('queue.queue', queue_id=queue_id))


@bp.route('/forget_queue', methods=['POST'])
def forget_queue():
    data = request.get_json(force=True)
    try:
        cur_queue = Queue.query.filter_by(id=data['queue_id']).first()
        cur_queue.remove_member(cur_user_or_temp(request))
        db.session.commit()
    except:
        return {}, 400
    return {}, 200


@bp.route('/kill_queue', methods=['POST'])
@login_required
@check_is_confirmed
def kill_queue():
    data = request.get_json(force=True)
    print(data)
    try:
        cur_queue = Queue.query.filter_by(id=data['queue_id']).first()
        if current_user == cur_queue.admin:
            Queue.query.filter_by(id=data['queue_id']).delete()
            db.session.commit()
        else:
            return {}, 400
    except:
        return {}, 400

    return {}, 200


@bp.route('/my_queues', methods=['GET'])
@login_required
@check_is_confirmed
def my_queues():
    kill_form = KillQueueForm()
    forget_form = ForgetQueueForm()
    return render_template('queue/my_queues.html',
                           kill_queue_form=kill_form,
                           forget_queue_form=forget_form)
