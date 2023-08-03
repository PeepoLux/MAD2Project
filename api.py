from flask_restful import Resource, fields, marshal_with, reqparse
from models import *
from database import db
from validation import NotFoundError, BusinessValidationError
from flask import jsonify, make_response, request, session

output_fields = {
	"venue_id": fields.Integer,
	"venue_name": fields.String,
	"venue_place": fields.String,
	"venue_city": fields.String,
	"venue_capacity": fields.Integer
}

output_fields_2 = {
	"venue_id": fields.Integer,
	"venue_name": fields.String,
	"venue_place": fields.String,
	"venue_city": fields.String,
	"venue_capacity": fields.Integer,
	"show_names": fields.List(fields.String)
}

create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument('name')
create_venue_parser.add_argument('place')
create_venue_parser.add_argument('city')
create_venue_parser.add_argument('capacity')

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('venue_name')


class VenueAPI(Resource):
	@marshal_with(output_fields_2)
	def get(self, venue_name):  # Get venue details

		venues = db.session.query(Venues).filter(
			Venues.venue_name == venue_name).first()

		if venues is None:
			raise NotFoundError(status_code=404)

		shows = db.session.query(Shows).filter(
			Shows.show_venue_id == venues.venue_id).all()
		if shows is None:
			shows_list = []
		else:
			shows_list = []
			for j in range(len(shows)):
				shows_list.append(shows[j].show_name)

		data = {"venue_id": venues.venue_id,
				"venue_name": venues.venue_name,
				"venue_place": venues.venue_place,
				"venue_city": venues.venue_city,
				"venue_capacity": venues.venue_capacity,
				"show_names": shows_list
				}
		return (data), 200

	@marshal_with(output_fields)
	def put(self, venue_name):  # Change the venue details
		args = create_venue_parser.parse_args()
		venue_name_provided = args.get("name", None)
		venue_place_provided = args.get("place", None)
		venue_city_provided = args.get("city", None)
		venue_capacity_provided = args.get("capacity", None)

		
		
		to_change = Venues.query.filter_by(venue_name=venue_name).first()

		if(to_change is None):
			raise BusinessValidationError(
				status_code=400, error_code="BE1001", error_message="Venue Name is required")
		if(venue_name_provided is not None):
			if(venue_name_provided != ""):
				to_change.venue_name = venue_name_provided
		if(venue_place_provided is not None):
			if(venue_place_provided != ""):
				to_change.venue_place = venue_place_provided
		if(venue_city_provided is not None):
			if(venue_city_provided != ""):
				to_change.venue_city = venue_city_provided
		if(venue_capacity_provided is not None):
			if(venue_capacity_provided != ""):
				to_change.venue_capacity = venue_capacity_provided
		
		db.session.add(to_change)
		db.session.commit()

		return to_change, 200

	def delete(self, venue_name): # Delete the venue
		to_remove = Venues.query.filter_by(venue_name=venue_name).first()
		if to_remove is None:
			raise NotFoundError(status_code=404)

		db.session.delete(to_remove)
		db.session.commit()

		return "Done", 200

	@marshal_with(output_fields)
	def post(self):  # Adding a new venue
		args = create_venue_parser.parse_args()
		name = args.get("name", None)
		place = args.get("place", None)
		city = args.get("city", None)
		capacity = args.get("capacity", None)

		if name is None or name == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE1001", error_message="Venue Name is required")

		if place is None or place == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE1002", error_message="Venue Place is required")

		if city is None or city == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE1003", error_message="Venue City is required")

		if capacity is None or capacity == "":  # name already exists
			raise BusinessValidationError(
				status_code=400, error_code="BE1004", error_message="Venue Capacity is required")

		# after all checks, add the venue
		add_details = Venues(venue_name=name, venue_place=place,
							 venue_city=city, venue_capacity=capacity)
		db.session.add(add_details)
		db.session.commit()
		return add_details, 201


output_fields_shows = {
	"show_id": fields.Integer,
	"show_name": fields.String,
	"show_venue_id": fields.Integer,
	"show_tags": fields.String,
	"show_price": fields.Integer,
	"show_rating": fields.Arbitrary,
	"show_start": fields.String,
	"show_end": fields.String,
	"show_booked": fields.Integer
}

output_fields_shows_1 = {
	"show_id": fields.Integer,
	"show_name": fields.String,
	"show_venue_id": fields.Integer,
	"show_tags": fields.String,
	"show_price": fields.Integer,
	"show_rating": fields.String,
	"show_start": fields.String,
	"show_end": fields.String,
	"booked": fields.Integer
}

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('show_name')
create_show_parser.add_argument('show_price')
create_show_parser.add_argument('show_start')
create_show_parser.add_argument('show_end')
create_show_parser.add_argument('show_tags')

add_show_parser = reqparse.RequestParser()
add_show_parser.add_argument('show_name')
add_show_parser.add_argument('show_venue_id')
add_show_parser.add_argument('show_tags')
add_show_parser.add_argument('show_price')
add_show_parser.add_argument('show_rating')
add_show_parser.add_argument('show_start')
add_show_parser.add_argument('show_end')

class ShowAPI(Resource):
	@marshal_with(output_fields_shows)
	def get(self, show_id):  # Get a venue

		shows = Shows.query.filter_by(show_id=show_id).first()

		if shows is None:
			raise NotFoundError(status_code=404)

		data = {"show_id": shows.show_id,
				"show_name": shows.show_name,
				"show_venue_id": shows.show_venue_id,
				"show_tags": shows.show_tags,
				"show_price": shows.show_price,
				"show_rating": shows.show_rating,
				"show_start": shows.show_start,
				"show_end": shows.show_end,
				"show_booked": shows.booked
				}
		return (data), 200

	@marshal_with(output_fields_shows_1)
	def put(self, show_id):  # Change Show Details
		args = create_show_parser.parse_args()
		show_name_provided = args.get("show_name", None)
		show_price_provided = args.get("show_price", None)
		show_start_provided = args.get("show_start", None)
		show_end_provided = args.get("show_end", None)
		show_tags_provided = args.get("show_tags", None)

		
		
		to_change_1 = Shows.query.filter_by(show_id=show_id).first()

		if(to_change_1 is None):
			raise BusinessValidationError(
				status_code=400, error_code="BE3001", error_message="No such show is found by that ID")
		if(show_name_provided is not None):
			if(show_name_provided != ""):
				to_change_1.show_name = show_name_provided
		if(show_price_provided is not None):
			if(show_price_provided != ""):
				to_change_1.show_price = show_price_provided
		if(show_start_provided is not None):
			if(show_start_provided != ""):
				to_change_1.show_start = show_start_provided
		if(show_end_provided is not None):
			if(show_end_provided != ""):
				to_change_1.show_end = show_end_provided
		if(show_tags_provided is not None):
			if(show_tags_provided != ""):
				to_change_1.show_tags = show_tags_provided
		
		db.session.add(to_change_1)
		db.session.commit()

		return to_change_1, 200

	def delete(self, show_id):
		to_remove = Shows.query.filter_by(show_id=show_id).first()
		if to_remove is None:
			raise NotFoundError(status_code=404)

		db.session.delete(to_remove)
		db.session.commit()

		return "Done", 200

	@marshal_with(output_fields_shows_1)
	def post(self):  # Adding a new Show
		args = add_show_parser.parse_args()
		show_name = args.get("show_name", None)
		show_venue_id = args.get("show_venue_id", None)
		show_tags = args.get("show_tags", None)
		show_price = args.get("show_price", None)
		show_rating = args.get("show_rating", None)
		show_start = args.get("show_start", None)
		show_end = args.get("show_end", None)


		if show_name is None or show_name == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE4001", error_message="Show Name is required")

		if show_venue_id is None or show_venue_id == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE4002", error_message="Show's Venue ID is required")

		if show_tags is None or show_tags == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE4003", error_message="Show Tags is required")

		if show_price is None or show_price == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE4004", error_message="Show Price is required")
		
		if show_rating is None or show_rating == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE4005", error_message="Show Rating is required")
		
		if show_start is None or show_start == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE4006", error_message="Show Start is required")
		
		if show_end is None or show_end == "":
			raise BusinessValidationError(
				status_code=400, error_code="BE4007", error_message="Show End is required")

		venues = Venues.query.filter_by(venue_id=show_venue_id).all()
		flag = 0
		for i in range(len(venues)):
			if(int(show_venue_id) == int(venues[i].venue_id)):
				flag = 1
		
		if(flag == 0):
			raise BusinessValidationError(
				status_code=400, error_code="BE4008", error_message="Such a Venue ID does not exist.")
			
		# after all checks, add the show
		add_details = Shows(show_name=show_name, 
		      				show_venue_id=show_venue_id,
							show_tags=show_tags, 
							show_price=show_price,
							show_rating=show_rating,
							show_start=show_start,
							show_end=show_end,
							booked=0
		)
		db.session.add(add_details)
		db.session.commit()
		return add_details, 201
	
# class GetNumber(Resource):
# 	def get(self):
# 		#Processing
# 		l1 = [[100,200,1,[[]]],[20,40,0,[[]]]]
# 		return make_response(jsonify({'value': l1}))
	
class List_Venues(Resource):
	def get(self):
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

			return make_response(jsonify({'error': error, 'city_search': city_search, 'rating_chosen': rating_chosen, 'tags_chosen': tags_chosen, 'city_chosen': city_chosen, 'tags_search': tags_search, 'name': session.get('name'),'output': output2, 'venuesExist': venuesExist, 'showsExist': showsExist, 'shows': output3}))
	
class MakeBooking(Resource):
	def get(self):
		show_id = request.headers.get('show_id')
		user_id = session.get('user_id')
		venue_id = request.headers.get("venue_id")
		quantity = request.headers.get("seats")
		available_seats = request.headers.get("available_seats")
		# error = 0
		if(int(quantity) > int(available_seats)):
			return ({"status":-1}),200
		else:
			add_details = Bookings(show_id=show_id, user_id=user_id,
								venue_id=venue_id, quantity=int(quantity))
			db.session.add(add_details)
			db.session.commit()

			to_change = Shows.query.filter_by(show_id=show_id).first()

			new_qty = int(to_change.booked) + int(quantity)
			to_change.booked = new_qty #Update the booking count.
			db.session.add(to_change)
			db.session.commit()
			# error=2
			return ({"status": 1}),200