from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from app import db
from app.main.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from werkzeug.urls import url_parse
from datetime import datetime
from app.main import bp


@bp.route('/')
@bp.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("You created the post!")
        return redirect(url_for('main.index'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Home', form=form, posts=posts)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid user or password')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if next_page is None or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', form=form, title='Sign in')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_anonymous and current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form, title='Register')


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, title='Edit Profile')


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@bp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users, title='Пользователи')


@bp.route('/follow/<username>')
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You can\'t follow yourself')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {} now'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if User is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash('You don\'t follow {}'.format(username))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You stopped following {}'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.after_request
def add_header(response):
    response.cache_control.private = True
    response.cache_control.public = False
    return response
