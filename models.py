from database import db
from sqlalchemy import PrimaryKeyConstraint, DateTime, desc
import datetime

class Users(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	name    = db.Column(db.String, index=True, unique=True)
	password = db.Column(db.String)

class Admins(db.Model):
	__tablename__ = 'admins'
	admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	name    = db.Column(db.String, index=True, unique=True)
	password = db.Column(db.String)
	
class Venues(db.Model):
	__tablename__ = 'venues'
	venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	venue_name = db.Column(db.String, index=True, unique=True)
	venue_place = db.Column(db.String)
	venue_city = db.Column(db.String, index=True)
	venue_capacity = db.Column(db.Integer)

class Shows(db.Model):
	__tablename__ = 'shows'
	show_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	show_name = db.Column(db.String, index=True)
	show_venue_id = db.Column(db.Integer)
	show_tags = db.Column(db.String, index=True)
	show_price = db.Column(db.Integer)
	show_rating = db.Column(db.Integer)
	show_start = db.Column(db.String)
	show_end = db.Column(db.String)
	booked = db.Column(db.Integer)

class Bookings(db.Model):
	__tablename__ = 'bookings'
	booking_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	show_id = db.Column(db.Integer, index=True)
	venue_id = db.Column(db.Integer, index=True)
	user_id = db.Column(db.Integer, index=True)
	quantity = db.Column(db.Integer)
	customer_rating = db.Column(db.Integer)

db.create_all()