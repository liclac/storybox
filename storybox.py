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

misaka = Misaka(app, **{i: True for i in app.config['MISAKA_EXTENSIONS']})

login_manager = LoginManager(app)
login_manager.login_view = 'login.login'
login_manager.login_message = u"You have to log in to access this."
login_manager.login_message_category = 'error'



# Note that we're not using URL prefixes - some blueprints need to react to
# multiple different URLs (such as the user one, which has both /u and /me)
from modules.login.login import mod as login_mod
app.register_blueprint(login_mod)

from modules.users.users import mod as users_mod
app.register_blueprint(users_mod)

from modules.stories.stories import mod as stories_mod
app.register_blueprint(stories_mod)

from modules.write.write import mod as write_mod
app.register_blueprint(write_mod)

from modules.help.help import mod as help_mod
app.register_blueprint(help_mod)



@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)

@app.template_filter()
def extract(d, key, default=None):
	if not key in d:
		return (default, d)
	else:
		val = d[key]
		del d[key]
		return (val, d)

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

@app.route('/about/')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
