from flask import Blueprint, current_app, render_template, abort

mod = Blueprint('help', __name__, template_folder='templates')

@mod.route('/h/')
def index():
	return render_template('help/index.html')

@mod.route('/h/<topic>')
def topic(topic):
	try:
		with current_app.open_resource('content/help/%s.md' % topic) as f:
			content = f.read()
			return render_template('help/topic.html', content=content)
	except Exception as e:
		print e
		abort(404)
