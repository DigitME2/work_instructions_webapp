from app.extensions import db
from app.login import bp
from app.login.forms import LoginForm, RegisterForm, ChangePasswordForm
from app.default.models import User
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """The screen to log the user into the system."""
    if current_user.is_authenticated:
        return redirect(url_for('default.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", category="top")
            return redirect(url_for('login.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('default.home')
        return redirect(next_page)
    nav_bar_title = "Login"
    return render_template('login.html', title='Sign in', form=form, nav_bar_title=nav_bar_title)


@bp.route('/logout')
def logout():
    """ Logs the user out of the system. """
    logout_user()
    return redirect(url_for('login.login'))


@bp.route('/newuser', methods=['GET', 'POST'])
@login_required
def new_user():
    """ The screen to register a new user."""

    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        redirect(url_for('default.admin_home'))
    nav_bar_title = "New User"
    return render_template("newuser.html", title="Register", nav_bar_title=nav_bar_title, form=form)


@bp.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
    """ The page to change a user's password. The user is passed to this page."""
    user = User.query.get_or_404(request.args.get('user_id'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        redirect(url_for('admin_home'))
    nav_bar_title = "Change password for " + str(user.username)
    return render_template("changepassword.html", nav_bar_title=nav_bar_title, user=user, form=form)
