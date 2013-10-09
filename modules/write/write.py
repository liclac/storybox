from flask import Blueprint, render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from forms import NewStoryForm, WriteForm
from models import db, Story, Page

mod = Blueprint('write', __name__, template_folder='templates')

@mod.route('/w/', methods=['GET', 'POST'])
@login_required
def index():
	form = NewStoryForm()
	stories = Story.query.all()
	if form.validate_on_submit():
		story = Story(current_user, form.title.data, form.description.data, form.anonymous.data)
		db.session.add(story)
		db.session.commit()
		return redirect(url_for('write.story', identifier=story.identifier))
	return render_template('write/index.html', form=form, stories=stories)

@mod.route('/w/<identifier>/', methods=['GET', 'POST'])
@login_required
def story(identifier):
	story = Story.query.filter_by(identifier=identifier).first()
	form = WriteForm()
	# For some reason, we can't set a default value after the field has been initialized,
	# so... let's put all the pages in BACKWARDS! :D
	form.prev_page.choices = [(page.id, page.title) for page in story.pages[::-1]] or [(-1, '-- No Other Pages --')]
	
	if form.validate_on_submit():
		prev_page = Page.query.filter_by(id=form.prev_page.data).first() if len(story.pages) > 0 else None
		page = Page(current_user, story, prev_page, form.title.data, form.text.data)
		db.session.add(page)
		db.session.commit()
		return redirect(url_for('stories.page', identifier=story.identifier, pageID=page.identifier))
	return render_template('write/story.html', story=story, form=form)
