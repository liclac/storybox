from flask import Flask, render_template, redirect, url_for, flash
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from flask.ext.misaka import Misaka
from models import *
from forms import *
from assets import *

app = Flask(__name__)
app.config.from_object("config")
app.config.from_object("keys")

db.init_app(app); db.app = app
assets.init_app(app)

misaka = Misaka(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = u"You have to log in to access this."
login_manager.login_message_category = 'error'

# Note that we're not using URL prefixes - some blueprints need to react to multiple
# different URLs (such as the user one, which has both /u and /me)
from modules.help.help import mod as help_mod
app.register_blueprint(help_mod)

@app.template_filter()
def extract(d, key, default=None):
	if not key in d:
		return (default, d)
	else:
		val = d[key]
		del d[key]
		return (val, d)

@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)

@app.context_processor
def context_processor():
	def flashed_message_class(category):
		map_ = {
			'message': 'info',
			'error': 'danger'
		}
		return map_[category] if category in map_ else category
	return {
		'flashed_message_class': flashed_message_class
	}

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/dashboard/')
@login_required
def dashboard():
	return render_template('dashboard.html')

@app.route('/s/')
def stories():
	return render_template('stories.html')

@app.route('/s/<identifier>')
def story(identifier):
	return render_template('story.html')

@app.route('/u/<username>/')
def user(username):
	user = User.by_username(username)
	if user.username != username:	# This guarantees that mistaken capitalization and such is corrected
		return redirect(url_for('user', username=user.username))
	return render_template('user.html', user=user)

@app.route('/me/')
@login_required
def me():
	return render_template('me.html', user=current_user)

@app.route('/me/edit/', methods=['GET', 'POST'])
@login_required
def me_edit():
	form = UserEditForm(obj=current_user.profile)
	if form.validate_on_submit():
		current_user.profile.name = form.name.data
		current_user.profile.bio = form.bio.data
		db.session.commit()
		return redirect(url_for('me'))
	return render_template('me_edit.html', user=current_user, form=form)

@app.route('/me/edit/login/', methods=['GET', 'POST'])
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
			return redirect('me')
	return render_template('me_edit_login.html', user=current_user, form=form)

@app.route('/w/', methods=['GET', 'POST'])
@login_required
def write():
	form = NewStoryForm()
	stories = Story.query.all()
	if form.validate_on_submit():
		story = Story(current_user, form.title.data, form.description.data, form.anonymous.data)
		db.session.add(story)
		db.session.commit()
		return redirect(url_for('write_story', identifier=story.identifier))
	return render_template('write.html', form=form, stories=stories)

@app.route('/w/<identifier>/', methods=['GET', 'POST'])
@login_required
def write_story(identifier):
	story = Story.query.filter_by(identifier=identifier).first()
	form = WriteForm()
	form.prev_page.choices = [(page.id, page.title) for page in story.pages]
	form.prev_page.default = len(form.prev_page.choices)
	return render_template('write_story.html', story=story, form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter(User.username==form.username.data).first()
		if user and user.check_password(form.password.data):
			login_user(user)
			return redirect(url_for('index'))
		else:
			flash(u'Invalid username or password', 'error')
	return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(form.username.data, form.password.data, form.name.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

