from flask import Blueprint, render_template, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from forms import LoginForm, RegisterForm
from models import db, User

mod = Blueprint('login', __name__, template_folder='templates')

@mod.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter(User.username==form.username.data).first()
		if user and user.check_password(form.password.data):
			login_user(user)
			return redirect(url_for('core.index'))
		else:
			flash(u'Invalid username or password', 'error')
	return render_template('login/login.html', form=form)

@mod.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('core.index'))

@mod.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(form.username.data, form.password.data, form.name.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('core.index'))
	return render_template('login/register.html', form=form)
