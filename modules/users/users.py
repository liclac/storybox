from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from forms import UserEditForm, UserEditLoginForm

mod = Blueprint('users', __name__, template_folder='templates')

@mod.route('/u/')
def index():
	return render_template('users/index.html')

@mod.route('/u/<username>/')
def user(username):
	user = User.by_username(username)
	if user.username != username:	# This guarantees that mistaken capitalization and such is corrected
		return redirect(url_for('.user', username=user.username))
	return render_template('users/user.html', user=user)

@mod.route('/me/')
@login_required
def me():
	return render_template('users/me.html', user=current_user)

@mod.route('/me/edit/', methods=['GET', 'POST'])
@login_required
def me_edit():
	form = UserEditForm(obj=current_user.profile)
	if form.validate_on_submit():
		current_user.profile.name = form.name.data
		current_user.profile.bio = form.bio.data
		db.session.commit()
		return redirect(url_for('me'))
	return render_template('users/me_edit.html', user=current_user, form=form)

@mod.route('/me/edit/login/', methods=['GET', 'POST'])
@login_required
def me_edit_login():
	form = UserEditLoginForm(obj=current_user)
	if form.validate_on_submit():
		if not current_user.check_password(form.old_password.data):
			form.old_password.errors.append('Incorrect Password')
		else:
			current_user.username = form.username.data
			current_user.set_password(form.password.data)
			db.session.commit()
			return redirect('.me')
	return render_template('users/me_edit_login.html', user=current_user, form=form)
