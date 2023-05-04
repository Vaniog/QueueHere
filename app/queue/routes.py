from flask import render_template, flash, redirect, url_for, request, current_app, abort
from flask_login import login_required, current_user
from flask_babel import _
from app.queue.models import Queue, UserQueue, QueueTask, TaskEnum
from app.auth.models import User
from app.auth.utils import cur_user_or_temp
from app.auth.decorators import check_is_confirmed
from app.extensions import db
from app.queue.forms import CreateQueueForm, JoinQueueForm, KillQueueForm, ForgetQueueForm
from app.queue import bp


@bp.route('/queue/<queue_id>', methods=['GET', 'POST'])
def queue(queue_id):
    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()
    join_form = JoinQueueForm()

    cur_user = cur_user_or_temp()

    if join_form.validate_on_submit():
        if not cur_queue.is_open:
            flash(_('Queue is closed.'), 'danger')
        else:
            if cur_queue.contains(cur_user):
                flash(_('You have already enter this queue.'), 'danger')
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
            flash(_(u'You cant create more %(max_queues) than  queues', max_queues=max_queues), 'danger')
            return redirect(url_for('queue.create_queue'))

        new_queue = Queue(name=form.name.data, admin=current_user)

        db.session.add(new_queue)
        db.session.commit()

        return redirect(url_for('queue.queue', queue_id=new_queue.id))
    return render_template('queue/create_queue.html', create_queue_form=form, title='Create Queue')


@bp.route('/leave_queue/<queue_id>')
def leave_queue(queue_id):
    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()

    cur_queue.leave_member(cur_user_or_temp())

    db.session.commit()
    return redirect(url_for('queue.queue', queue_id=queue_id))


@bp.route('/forget_queue', methods=['POST'])
def forget_queue():
    data = request.get_json(force=True)
    try:
        cur_queue = Queue.query.filter_by(id=data['queue_id']).first()
        cur_queue.remove_member(cur_user_or_temp())
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


@bp.route('/manage_queue/<queue_id>', methods=['GET'])
@login_required
@check_is_confirmed
def manage_queue(queue_id):
    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()
    if cur_queue.admin != current_user:
        abort(404)

    return render_template('queue/manage_queue.html', queue=cur_queue)


@bp.route('/spam_queue/<queue_id>', methods=['GET'])
@login_required
def spam_queue(queue_id):
    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()
    for i in range(2, 7):
        spamer = User.query.filter_by(id=i).first()
        cur_queue.add_member(spamer, spamer.username)
    db.session.commit()
    return redirect(url_for('queue.manage_queue', queue_id=queue_id))


@bp.route('/update_queue/new_order', methods=['POST'])
@login_required
@check_is_confirmed
def new_order():
    data = request.get_json(force=True)
    queue_id = data['queue_id']

    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()

    if cur_queue.admin != current_user:
        abort(400)

    order = data['new_order']

    users_queue = cur_queue.list()
    old_indices = []
    for user_queue in users_queue:
        old_indices.append(user_queue.index_in_queue)
        user_queue.is_visible = False
    new_users_queue = []

    for i in order:
        new_users_queue.append(UserQueue.query.filter_by(queue_id=queue_id, member_id=int(i)).first_or_404())

    for i in range(len(new_users_queue)):
        new_users_queue[i].index_in_queue = old_indices[i]
        new_users_queue[i].is_visible = True

    db.session.commit()
    return {}, 200


@bp.route('/update_queue/open_queue', methods=['POST'])
@login_required
@check_is_confirmed
def open_queue():
    data = request.get_json(force=True)
    queue_id = data['queue_id']

    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()

    if cur_queue.admin != current_user:
        abort(400)

    cur_queue.open()
    db.session.commit()
    return {}, 200


@bp.route('/update_queue/close_queue', methods=['POST'])
@login_required
@check_is_confirmed
def close_queue():
    data = request.get_json(force=True)
    queue_id = data['queue_id']

    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()

    if cur_queue.admin != current_user:
        abort(400)

    cur_queue.close()
    db.session.commit()
    return {}, 200


@bp.route('/update_queue/add_task', methods=['POST'])
@login_required
@check_is_confirmed
def add_task():
    data = request.get_json(force=True)
    queue_id = data['queue_id']

    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()

    if cur_queue.admin != current_user:
        abort(400)

    task_action = data['task_action']
    task_time = data['task_time']
    if TaskEnum[task_action] is None:
        abort(400)
    task = QueueTask(queue_id=queue_id,
                     action=TaskEnum[task_action])
    try:
        task.execute_time = task_time
    except:
        abort(400)

    db.session.add(task)
    db.session.commit()

    return {}, 200


@bp.route('/get_queue_tasks/<queue_id>', methods=['POST', 'GET'])
@login_required
@check_is_confirmed
def get_queue_tasks(queue_id):
    cur_queue = Queue.query.filter_by(id=queue_id).first_or_404()

    res = []
    for task in cur_queue.tasks_sorted():
        res.append({
            'task_action': str(task.action),
            'task_time': task.execute_time,
            'task_id': task.id
        })
    return res, 200


@bp.route('/delete_queue_task', methods=['POST', 'GET'])
@login_required
@check_is_confirmed
def delete_queue_task():
    data = request.get_json(force=True)
    task_id = data['task_id']
    task = QueueTask.query.filter_by(id=task_id).first_or_404()

    if task.queue.admin_id != current_user.id:
        abort(400)

    QueueTask.query.filter_by(id=task_id).delete()
    db.session.commit()

    return {}, 200
