from flask import Blueprint, render_template

mod = Blueprint('core', __name__, template_folder='templates')

@mod.route('/')
def index():
	return render_template('core/index.html')

@mod.route('/about/')
def about():
	return render_template('core/about.html')
