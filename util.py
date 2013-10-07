import string
import random

def random_string(length):
	possible_characters = string.ascii_letters + string.digits
	return ''.join(random.choice(possible_characters) for _ in range(length))
