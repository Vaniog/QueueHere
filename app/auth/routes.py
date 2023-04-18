from app.auth import bp
from flask import redirect, flash, url_for, request, render_template
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, login_required, logout_user
from flask_babel import _
from app.auth.utils import generate_token, confirm_token, send_email
from app.auth.models import User
from app.auth.forms import LoginForm, RegistrationForm
from app.extensions import db
from datetime import datetime


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid user or password'), 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        next_page = request.args.get('next')
        if next_page is None or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', login_form=form, title='Sign in')


@bp.route('/logout')
@login_required
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

        token = generate_token(new_user.email)
        confirm_url = url_for("auth.confirm_email", user_id=new_user.id, token=token, _external=True)
        html = render_template("auth/confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(new_user.email, subject, html)

        login_user(new_user)

        flash(_('Congratulations, you are now a registered user! Check your email for verification.'), 'success')
        return redirect(url_for('auth.inactive'))
    return render_template('auth/register.html', register_form=form, title='Register')


@bp.route("/inactive")
@login_required
def inactive():
    if current_user.is_confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/inactive.html")


@bp.route("/resend_confirmation")
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        flash(_("Your account has already been confirmed.", "success"))
        return redirect(url_for("main.index"))

    token = generate_token(current_user.email)
    confirm_url = url_for("auth.confirm_email", user_id=current_user.id, token=token, _external=True)
    html = render_template("auth/confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)

    flash(_("A new confirmation email has been sent."), "success")
    return redirect(url_for("auth.inactive"))


@bp.route("/confirm_email/<user_id>/<token>")
def confirm_email(user_id, token):
    user = User.query.filter_by(id=user_id).first_or_404()
    if user.is_confirmed:
        flash(_("Account already confirmed."), "success")
        return redirect(url_for("main.index"))
    email = confirm_token(token)
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash(_("You have confirmed your account. Thanks!"), "success")
    else:
        flash(_("The confirmation link is invalid or has expired."), "danger")
    return redirect(url_for("main.index"))
