from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from passlib.context import CryptContext
from util import *

db = SQLAlchemy()

pwd_context = CryptContext(
	schemes = ['pbkdf2_sha256'],
	default = 'pbkdf2_sha256',
	all__vary_rounds = 0.1,
	pbkdf_sha256__default_rounds = 8000
)

story_contributors_table = db.Table('story_contributors',
	db.Column('story_id', db.Integer, db.ForeignKey('story.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), nullable=False, unique=True, index=True)
	password = db.Column(db.String(100), nullable=False)
	profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
	profile = db.relationship('Profile', uselist=False, backref='user', lazy='joined')
	
	def __init__(self, username, password, name, bio=''):
		self.username = username
		self.set_password(password)
		self.profile = Profile(name, bio)
	
	def set_password(self, password):
		self.password = pwd_context.encrypt(password)
	
	def check_password(self, password):
		return pwd_context.verify(password, self.password)
	
	@classmethod
	def by_username(cls, username):
		return cls.query.filter(db.func.lower(cls.username) == db.func.lower(username)).first()

class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(25), nullable=False)
	bio = db.Column(db.Text)
	
	def __init__(self, name, bio=''):
		self.name = name
		self.bio = bio

class Story(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	identifier = db.Column(db.String(20), unique=True, nullable=False, index=True)
	author = db.relationship('User', backref=db.backref('owned_stories', lazy='dynamic'))
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(255))
	anonymous = db.Column(db.Boolean)
	
	def __init__(self, author, title, description, anonymous):
		self.identifier = self.__class__.gen_identifier()
		self.author = author
		self.title = title
		self.description = description
		self.anonymous = anonymous
	
	@classmethod
	def gen_identifier(cls):
		length = 5
		tries = 0
		found_one = False
		while not found_one:
			candidate = random_string(length)
			if cls.query.filter(cls.identifier==candidate).count() != 0:
				tries += 1
				if tries > 50:
					length += 1
			else:
				return candidate

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	identifier = db.Column(db.String(20), nullable=False, index=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	author = db.relationship('User', backref=db.backref('pages', lazy='dynamic'))
	story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
	story = db.relationship('Story', backref='pages', lazy='joined')
	prev_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), index=True)
	prev_page = db.relationship('Page', backref=db.backref('following_pages', remote_side=[id]), lazy='dynamic')
	title = db.Column(db.String(100), nullable=False)
	text = db.Column(db.Text, nullable=False)
	
	__table_args__ = (
		db.UniqueConstraint('story_id', 'identifier', name='_page_story_identifier'),
	)
	
	def __init__(self, author, story, prev_page, title, text):
		self.identifier = self.__class__.gen_identifier(story)
		self.author = author
		self.story = story
		self.prev_page = prev_page
		self.title = title
		self.text = text
	
	@classmethod
	def gen_identifier(cls, story):
		length = 5
		tries = 0
		found_one = False
		while not found_one:
			candidate = random_string(length)
			if cls.query.filter((cls.story == story) & (cls.identifier == candidate)).count() != 0:
				tries += 1
				if tries > 50:
					length += 1
			else:
				return candidate
