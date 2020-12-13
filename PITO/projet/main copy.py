from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
api = Api(app)

class ClientModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	mail = db.Column(db.String(100))

	def __repr__(self):
		return f("Client (nom = {self.name}, mail = {self.mail})")

class TicketModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	code= db.Column(db.String)
	departure_airport_code= db.Column(db.String)
	arrival_airport_code = db.Column(db.String)
	price = db.Column(db.Integer)
	plane = db.relationship('PlaneModel', lazy='select', backref=db.backref('ticketModel', lazy='joined'))
	available=db.Column(db.Integer)

	def __repr__(self):
		return f("Ticket (code = {self.code}, departure_airport_code = {self.departure_airport_code}, arrival_airport_code = {self.arrival_airport_code}, price = {self.price}, plane = {self.plane}, available = {self.available}")

class PlaneModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	seats = db.Column(db.Integer)
	flight = db.Column(db.Integer, db.ForeignKey('ticketModel.id'), nullable=False)
	
	def __repr__(self):
		return f("Plane (name = {self.name}, seats = {self.seats}, flight = {self.flight})")


db.create_all()

Ticket_put_args = reqparse.RequestParser()
Ticket_put_args.add_argument(
    "id", type=str,  help="ID nombre unique pour un Ticket", required=True)
Ticket_put_args.add_argument(
    "date_entree_api", type=str, help="Date de création dans l'api", required=True)
Ticket_put_args.add_argument(
    "date_departure", type=str, help="Date de départ du vol", required=True)
Ticket_put_args.add_argument(
    "date_arrival", type=str, help="Date d'arrivée du vol", required=True)
Ticket_put_args.add_argument(
    "reservation", type=bool, help="Savoir si un Ticket est reserve ou pas", required=True)
Ticket_put_args.add_argument(
    "code_depart", type=str, help="Abréviation de l'aéroport de depart", required=True)
Ticket_put_args.add_argument("code_destination", type=str,
                             help="Abréviation de l'aéroport d'arrive", required=True)
Ticket_put_args.add_argument(
    "price", type=int, help="Prix du Ticket en euro", required=True)


Ticket_update_args = reqparse.RequestParser()
Ticket_update_args.add_argument(
    "id", type=int, help="ID nombre unique pour un Ticket", required=True)
Ticket_update_args.add_argument(
    "date_entree_api", type=str, help="Date de création dans l'api", required=True)
Ticket_update_args.add_argument(
    "date_departure", type=str, help="Date de départ du vol", required=True)
Ticket_update_args.add_argument(
    "date_arrival", type=str, help="Date d'arrivée du vol", required=True)
Ticket_update_args.add_argument(
    "reservation", type=bool, help="Savoir si un Ticket est reserve ou pas", required=True)
Ticket_update_args.add_argument(
    "code_depart", type=str, help="Abréviation de l'aéroport de depart", required=True)
Ticket_update_args.add_argument(
    "code_destination", type=str, help="Abréviation de l'aéroport d'arrive", required=True)
Ticket_update_args.add_argument(
    "prix", type=int, help="Prix du Ticket en euro", required=True)
Ticket_update_args.add_argument(
    "name", type=str, help="Nom du propriétaire du Ticket", required=True)

resource_fields = {
	'id': fields.Integer,
	'date_entree_api': fields.String,
	'date_departure': fields.String,
	'date_arrival': fields.String,
	'reservation': fields.Boolean,
	'code_depart': fields.String,
	'code_destination': fields.String,
	'prix': fields.Integer,
	'name': fields.String,
}

resource_fields_code = {
	'trajet_id': fields.Integer,
	'code_depart': fields.String,
	'code_destination': fields.String,
}


class Ticket(Resource):
	@marshal_with(resource_fields)
	def get(self, Ticket_id):
		result = TicketModel.query.filter_by(id=Ticket_id).first()
		if not result:
			abort(404, message="Could not find Ticket with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, Ticket_id):
		args = Ticket_put_args.parse_args()
		result = TicketModel.query.filter_by(id=Ticket_id).first()
		if result:
			abort(409, message="Ticket id taken...")

		Ticket = TicketModel(id=Ticket_id, date_entree_api=args['date_entree_api'], reservation=args['reservation'],
		                     code_depart=args['code_depart'], code_destination=args['code_destination'], prix=args['prix'], name=args['name'])
		db.session.add(Ticket)
		db.session.commit()
		return Ticket, 201

	@marshal_with(resource_fields)
	def patch(self, Ticket_id):
		args = Ticket_update_args.parse_args()
		result = TicketModel.query.filter_by(id=Ticket_id).first()
		if not result:
			abort(404, message="Ticket doesn't exist, cannot update")

		if args['id']:
			result.name = args['id']
		if args['date_entree_api']:
			result.views = args['date_entree_api']
		if args['date_departure']:
			result.views = args['date_departure']
		if args['date_arrival']:
			result.views = args['date_arrival']
		if args['reservation']:
			result.likes = args['reservation']
		if args['code_depart']:
			result.name = args['code_depart']
		if args['code_destination']:
			result.views = args['code_destination']
		if args['prix']:
			result.likes = args['prix']
		if args['name']:
			result.likes = args['name']

		db.session.commit()

		return result


class Find_Ticket_by_id(Resource):
	@marshal_with(resource_fields)
	def get(self, Ticket_id):
		result = TicketModel.query.filter_by(id=Ticket_id).all()
		if not result:
			abort(404, message="Could not find Ticket with that id")
		return result


class Find_Ticket_by_date(Resource):
	@marshal_with(resource_fields)
	def get(self, date):
		result = TicketModel.query.filter_by(date_entree_api=date).all()
		if not result:
			abort(404, message="Could not find Ticket with that date")
		return result


class Find_Ticket_by_date_dep(Resource):
	@marshal_with(resource_fields)
	def get(self, date):
		result = TicketModel.query.filter_by(date_departure=date).all()
		if not result:
			abort(404, message="Could not find Ticket with that departure date")
		return result


class Find_Ticket_by_date_arr(Resource):
	@marshal_with(resource_fields)
	def get(self, date):
		result = TicketModel.query.filter_by(date_arrival=date).all()
		if not result:
			abort(404, message="Could not find Ticket with that arrival date")
		return result


class Find_Ticket_by_max_price(Resource):
	@marshal_with(resource_fields)
	def get(self, price):
		result = TicketModel.query.filter_by(prix=price).all()
		if not result:
			abort(404, message="Could not find Ticket with that arrival date")
		return result

class Find_available_departure(Resource):
	@marshal_with(resource_fields_code)
	def get(self):
		allCodes = CodeModel.query.filter_by().all()
		for i in range(len(allCodes)):
		  if len(TicketModel.query.filter_by(id_trajet=i).filter_by(reservation=0).all())==0:
			  allCodes[i].remove()
		if not allCodes:
  			abort(404, message="Could not find Codes")
		return allCodes


class All_Ticket(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = TicketModel.query.filter_by().all()
		if not result:
			abort(404, message="Could not find No Ticket")
		return result


api.add_resource(Ticket, "/Ticket/<int:Ticket_id>")
api.add_resource(All_Ticket, "/Tickets")
api.add_resource(Find_available_departure, "/available_departure")
api.add_resource(Find_Ticket_by_id, "/Ticket_id/<int:Ticket_id>")
api.add_resource(Find_Ticket_by_date, "/Ticket_entree_api/<string:date_entree_api>")
api.add_resource(Find_Ticket_by_date_dep, "/Ticket_departure_date/<string:date_departure>")
api.add_resource(Find_Ticket_by_date_arr, "/Ticket_arrival_date/<string:date_arrival>")
api.add_resource(Find_Ticket_by_max_price, "/Ticket_price/<string:price>")



if __name__ == "__main__":
	app.run(debug=True)
