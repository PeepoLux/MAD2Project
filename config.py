import os

current_dir = os.path.abspath(os.path.dirname(__file__))

class Config():
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = None
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = None

class LocalDevelopmentConfig(Config):
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(current_dir, "db2.sqlite3")
	SECRET_KEY = 'thisisasecretkey'
	DEBUG = True

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(current_dir, "proddb.sqlite3")
	SECRET_KEY = 'thisisasecretkey'
	DEBUG = False
