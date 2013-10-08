from flask import Blueprint, render_template, redirect, url_for
from models import Story, Page

mod = Blueprint('stories', __name__, template_folder='templates')

@mod.route('/s/')
def index():
	stories = Story.query.all()
	return render_template('stories/index.html', stories=stories)

@mod.route('/s/<identifier>/')
def story(identifier):
	story = Story.query.filter_by(identifier=identifier).first()
	return render_template('stories/story.html', story=story)

@mod.route('/s/<identifier>/<pageID>')
def page(identifier, pageID):
	story = Story.query.filter_by(identifier=identifier).first()
	page = Page.query.filter_by(story=story, identifier=pageID).first()
	return render_template('stories/page.html', story=story, page=page)
