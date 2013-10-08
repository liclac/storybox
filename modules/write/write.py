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
	form.prev_page.choices = [(page.id, page.title) for page in story.pages] or [('', '-- No Other Pages --')]
	#form.prev_page.default = len(form.prev_page.choices)-1
	if form.validate_on_submit():
		page = Page(current_user, story, form.prev_page.data, form.text.data)
		print page
		db.session.add(page)
		db.session.commit()
		return redirect(url_for('stories.page', identifier=story.identifier, pageID=page.identifier))
	else:
		for field in form.errors:
			flash('%s: %s' % (field, form.errors[field]), 'error')
	return render_template('write/story.html', story=story, form=form)
