import datetime
#pip install flask-bcrypt
#pip install flask-login
#pip install flask-wtf
#pip install peewee
from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('social.db') #janine

class User(UserMixin, Model):
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField(max_length = 100) 
	joined_at = DateTimeField(default = datetime.datetime.now)
	is_admin = BooleanField(default = False)
	
	class Meta:
		database = DATABASE
		order_by = ('-joined_at',)
		
	@classmethod
	def create_user(cls, username, email, password, admin=False):
		try:
			cls.create(
				username = username, 
				email = email,
				password = generate_password_hash(password),
				is_admin = admin)
		except IntegrityError:
			raise ValueError("User already exists")
			
def initialize():
	DATABASE.connect() #janine
	DATABASE.create_tables([User], safe = True) 
	DATABASE.close()