import os

# Database connection information
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.dirname(__file__), 'db.sqlite')

# Enable Misaka extensions from this list
MISAKA_EXTENSIONS = [
	'tables',			# Enables the use of PHP-Markdown style tables
	'strikethrough',	# Enables ~~strikethrough~~
	'hard_wrap',		# Makes newlines in markdown insert newlines in the rendered text
]
