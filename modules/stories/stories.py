from flask import Blueprint, render_template, redirect, url_for

mod = Blueprint('stories', __name__, template_folder='templates')

@mod.route('/s/')
def index():
	return render_template('stories/index.html')

@mod.route('/s/<identifier>')
def story(identifier):
	return render_template('stories/story.html')
