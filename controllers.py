from flask import Flask, flash, redirect, url_for, session, render_template, request
from flask import current_app as app
from models import *
from base64 import b64encode
import datetime
import re


@app.route('/', methods=['GET', 'POST'])
def index():
	error = None
	if request.method == "GET":
		return render_template('login.html')
	elif request.method == "POST":
		name = request.form["username"]
		password = request.form["password"]

		user = Users.query.filter_by(name=name).first()
		if user is None:  # new user
			error = "Username not found! Please try again or Register"
			flash(error, "error")
			return render_template('login.html', name=name)
		else:  # old user

			if (user.password == password):  # sucessful login
				session['name'] = name
				session['user_id'] = user.user_id
				return redirect(url_for('userhome', error=0, city="None", tags="None", rating=0))
			else:  # wrong password
				flash("Wrong Password. Please register if you haven't already!")
				return redirect(url_for('index'))

		return render_template('login.html', name=name, error=error)
	else:
		print("Error check")


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminindex():
	error = None
	if request.method == "GET":
		return render_template('adminlogin.html')
	elif request.method == "POST":
		name = request.form["username"]
		password = request.form["password"]

		admin = Admins.query.filter_by(name=name).first()
		if admin is None:  # new user
			error = "Username not found! Please try again"
			flash(error, "error")
			return render_template('adminlogin.html', name=name)
		else:  # old user

			if (admin.password == password):  # sucessful login
				session['admin_name'] = name
				session['admin_user_id'] = admin.admin_id
				return redirect(url_for('admindashboard'))
			else:  # wrong password
				flash("Wrong Password. Please register if you haven't already!")
				return redirect(url_for('adminindex'))

		return render_template('adminlogin.html', name=name, error=error)
	else:
		print("Error check")


@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == "GET":
		return render_template('register.html')
	elif request.method == "POST":
		name = request.form["username"]
		password = request.form["password"]

		pattern = re.compile(
			'^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
		result = pattern.match(password)

		user = Users.query.filter_by(name=name).first()
		if user is None and result is not None:
			add_name = Users(name=name, password=password)
			if len(name) >= 3:
				db.session.add(add_name)
				db.session.commit()
				flash("Registration Successful! Please login to continue.")
				return redirect(url_for('index'))
			else:
				flash("Please make sure the username has atleast 5 characters")
				return redirect(url_for('register'))
		elif user is not None:
			flash("Username already exists!")
			return redirect(url_for('register'))
		elif result is None:
			flash("Please make sure the password satisfied all the conditions:")
			flash("Minimum length is 6 and Maximum length is 20.")
			flash("Includes atleast a digit number.")
			flash("Includes atleast a lowercase and an uppercase letter.")
			flash("Includes atleast a special character.")
			return redirect(url_for('register'))


@app.route('/addvenue', methods=['POST'])
def addvenue():
	name = request.form["name"]
	place = request.form["place"]
	city = request.form["city"]
	capacity = request.form["capacity"]

	add_details = Venues(venue_name=name, venue_place=place,
						 venue_city=city, venue_capacity=capacity)
	db.session.add(add_details)
	db.session.commit()

	return redirect(url_for('admindashboard'))


@app.route('/addshow', methods=['POST'])
def addshow():
	name = request.form["name"]
	tags = request.form["tags"]
	price = request.form["price"]
	rating = request.form["rating"]
	start = request.form["start"]
	end = request.form["end"]
	venue_id = request.form["venue_id"]

	add_details = Shows(show_venue_id=venue_id, show_name=name,
						show_tags=tags, show_price=price, show_rating=rating,
						show_start=start, show_end=end, booked=0)
	db.session.add(add_details)
	db.session.commit()

	return redirect(url_for('admindashboard'))


@app.route('/editvenue', methods=["POST"])
def venueedit():
	name = request.form["name"]
	place = request.form["place"]
	city = request.form["city"]
	capacity = request.form["capacity"]
	venue_id = request.form["venue_id"]
	to_change = Venues.query.filter_by(venue_id=venue_id).first()

	to_change.venue_name = name
	to_change.venue_place = place
	to_change.venue_capacity = capacity
	to_change.venue_city = city
	db.session.add(to_change)
	db.session.commit()
	return redirect(url_for('admindashboard'))

@app.route('/editshow', methods=["POST"])
def showedit():
	show_id = request.form["show_id"]
	name = request.form["name"]
	tags = request.form["tags"]
	price = request.form["price"]
	rating = request.form["rating"]
	start = request.form["start"]
	end = request.form["end"]
	to_change = Shows.query.filter_by(show_id=show_id).first()

	to_change.show_name = name
	to_change.show_tags = tags
	to_change.show_price = price
	to_change.show_rating = rating
	to_change.show_start = start
	to_change.show_end = end
	db.session.add(to_change)
	db.session.commit()
	return redirect(url_for('admindashboard'))


@app.route('/deletevenue', methods=["POST"])
def venuedelete():
	venue_id = request.form["venue_id"]

	to_remove = Venues.query.filter_by(venue_id=venue_id).first()
	db.session.delete(to_remove)
	db.session.commit()

	return redirect(url_for('admindashboard'))


@app.route('/deleteshow', methods=["POST"])
def showdelete():
	show_id = request.form["show_id"]

	to_remove = Shows.query.filter_by(show_id=show_id).first()
	db.session.delete(to_remove)
	db.session.commit()

	return redirect(url_for('admindashboard'))


@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
	if request.method == "GET":
		if session.get('admin_name') is not None:
			venues = Venues.query.all()
			
			li2, output2, output3, showsExist = [], [], [], []
			for i in range(len(venues)):
				li = []
				li.append(venues[i].venue_name)
				li.append(venues[i].venue_place)
				li.append(venues[i].venue_city)
				li.append(venues[i].venue_capacity)
				li.append(venues[i].venue_id)

				shows = Shows.query.filter_by(
					show_venue_id=venues[i].venue_id).all()
				if (len(shows) > 0):
					li.append(1)
				else:
					li.append(0)
				temp = []
				for j in range(len(shows)):
					li3 = []
					li3.append(shows[j].show_name)
					li3.append(shows[j].show_tags)
					li3.append(shows[j].show_price)
					li3.append(shows[j].show_rating)
					li3.append(shows[j].show_start)
					li3.append(shows[j].show_end)
					li3.append(shows[j].show_id)
					temp.append(li3)
				li.append(temp)
				output2.append(li)
				li2 = []
			print(output2)
			venuesExist = 0
			if len(venues) > 0:
				venuesExist = 1

			return render_template('admindashboard.html', output=output2, venuesExist=venuesExist, showsExist=showsExist, shows=output3, user_id=session.get('user_id'))
		else:
			flash("Unauthorized Access!")
			return redirect(url_for('adminindex'))

@app.route('/home', methods=['GET', 'POST'])
def userhome():
	if request.method == "GET":
		if session.get('name') is not None:
			venues = Venues.query.all()
			error = int(request.args.get('error'))
			try:
				city_chosen = request.args.get('city')
			except:
				city_chosen = None
			
			try:
				tags_chosen = request.args.get('tags')
			except:
				tags_chosen = None
			
			try:
				rating_chosen = request.args.get('rating')
			except:
				rating_chosen = 0
			
			li2, output2, output3, showsExist = [], [], [], []
			for i in range(len(venues)):
				
				# INOX
				li = [venues[i].venue_name, venues[i].venue_place, venues[i].venue_city, 
	  				  venues[i].venue_capacity, venues[i].venue_id]

				shows = Shows.query.filter_by(show_venue_id=venues[i].venue_id).all()
				if (len(shows) > 0):
					li.append(1)
				else:
					li.append(0)
				temp = []
				for j in range(len(shows)):
					li3 = []
					li3.append(shows[j].show_name)
					li3.append(shows[j].show_tags)
					li3.append(shows[j].show_price)
					li3.append(str(shows[j].show_rating))
					li3.append(shows[j].show_start)
					li3.append(shows[j].show_end)
					li3.append(shows[j].show_id)
					li3.append(venues[i].venue_capacity - shows[j].booked) #available seats
					temp.append(li3)
				li.append(temp)
				output2.append(li)
				li2 = []
			print(output2)
			venuesExist = 0
			if len(venues) > 0:
				venuesExist = 1
			
			city_search = set()
			for i in range(len(venues)):
				city_search.add(venues[i].venue_city)

			tags_search = set()
			shows_all = Shows.query.all()
			for i in range(len(shows_all)):
				tags_search.add(shows_all[i].show_tags)
			

			print(output2)
			return render_template('userhome.html', error=error, city_search=city_search, rating_chosen = rating_chosen, tags_chosen = tags_chosen, city_chosen = city_chosen, tags_search = tags_search, name=session.get('name'),output=output2, venuesExist=venuesExist, showsExist=showsExist, shows=output3)
		else:
			flash("Unauthorized Access!")
			return redirect(url_for('index'))
		
@app.route('/booking', methods=["GET","POST"])
def booking():
	show_id = request.form["show_id"]
	user_id = session.get('user_id')
	venue_id = request.form["venue_id"]
	quantityy = request.form["seats"]
	available_seatss = request.form["available_seatss"]
	error = 0
	if(int(quantityy) > int(available_seatss)):
		error = 1
		return redirect(url_for('userhome',error=error))
	else:
		add_details = Bookings(show_id=show_id, user_id=user_id,
							venue_id=venue_id, quantity=int(quantityy))
		db.session.add(add_details)
		db.session.commit()

		to_change = Shows.query.filter_by(show_id=show_id).first()

		new_qty = int(to_change.booked) + int(quantityy)
		to_change.booked = new_qty #Update the booking count.
		db.session.add(to_change)
		db.session.commit()
		error=2
		return redirect(url_for('userhome', error=error))

@app.route('/mybookings', methods=["GET","POST"])
def mybookings():
	if request.method == "GET":
		if session.get('name') is not None:
			error = int(request.args.get('error'))
			bookings_to_display = db.session.query(Bookings,Shows, Venues).filter(Bookings.show_id == Shows.show_id).filter(Bookings.venue_id == Venues.venue_id).filter(Bookings.user_id == session.get('user_id')).order_by(desc(Bookings.booking_id)).all()
			output = []
			for i in range(len(bookings_to_display)):
				li = []
				li.append(bookings_to_display[i][0].booking_id)
				li.append(bookings_to_display[i][0].quantity)
				li.append(bookings_to_display[i][1].show_name)
				li.append(bookings_to_display[i][1].show_tags)
				li.append(bookings_to_display[i][1].show_start)
				li.append(bookings_to_display[i][1].show_end)
				li.append(bookings_to_display[i][2].venue_name)
				li.append(bookings_to_display[i][2].venue_place)
				li.append(bookings_to_display[i][2].venue_city)
				li.append(bookings_to_display[i][0].customer_rating)
				output.append(li)
			
			return render_template('mybookings.html', output=output, error=error)
		else:
			flash("Unauthorized Access!")
			return redirect(url_for('index'))
		
@app.route('/rating', methods=["GET","POST"])
def rating():
	booking_id = request.form["booking_id"]
	customer_rating = request.form["rating"]

	to_change = Bookings.query.filter_by(booking_id=booking_id).first()
	to_change.customer_rating = customer_rating
	db.session.add(to_change)
	db.session.commit()
	return redirect(url_for('mybookings',error=0))

@app.route('/logout')
def logout():
	session['user_id'] = None
	session['name'] = None
	session['admin_user_id'] = None
	session['admin_name'] = None
	flash('Have a nice day!')
	return redirect(url_for('index'))
