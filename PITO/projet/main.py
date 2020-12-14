from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

association_table = db.Table('association',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
    db.Column('flight_code', db.String, db.ForeignKey('flight.code'))
)

class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	mail = db.Column(db.String(100))
	nationality = db.Column(db.String(100))
	tickets = db.relationship('Flight', secondary=association_table)

	def __repr__(self):
		return f("Client (nom = {self.name}, mail = {self.mail}, tickets = {self.tickets})")

class Flight(db.Model):
	code = db.Column(db.String,primary_key=True)
	date = db.Column(db.String)
	departure_airport_code= db.Column(db.String)
	arrival_airport_code = db.Column(db.String)
	price = db.Column(db.Integer)
	plane_id = db.Column(db.Integer, db.ForeignKey('plane.id'))
	plane = db.relationship('Plane', lazy='select',uselist=False, backref=db.backref('flight', lazy='joined'))

	available=db.Column(db.Integer)

	def __repr__(self):
		return f("Flight (code = {self.code}, date = {self.date}, departure_airport_code = {self.departure_airport_code}, arrival_airport_code = {self.arrival_airport_code}, price = {self.price}, plane = {self.plane}, available = {self.available}")


class Plane(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	seats = db.Column(db.Integer)
	
	def __repr__(self):
		return f("Plane (name = {self.name}, seats = {self.seats})")

db.create_all()

Flight_put_args = reqparse.RequestParser()
Flight_put_args.add_argument("code", type=str,  help="Flight code", required=True)
Flight_put_args.add_argument("departure_airport_code", type=str,  help="Departure Airport code", required=True)
Flight_put_args.add_argument("arrival_airport_code", type=str,  help="Arrival airport code", required=True)
Flight_put_args.add_argument("price", type=int,  help="Flight ticket price", required=True)
Flight_put_args.add_argument("plane", type=int,  help="Flight ticket price", required=False)

Client_put_args = reqparse.RequestParser()
Client_put_args.add_argument("name", type=str,  help="Flight code", required=True)
Client_put_args.add_argument("mail", type=str,  help="Flight code", required=True)
Client_put_args.add_argument("nationality", type=str,  help="Flight code", required=True)


resource_fields_plane = {
	'name': fields.String,
	'seats': fields.Integer
}

resource_fields = {
	'id': fields.Integer,
	'code' : fields.String,
	'date' : fields.String,
	'departure_airport_code' : fields.String,
	'arrival_airport_code' : fields.String,
	'price' : fields.String,
	'plane' : fields.Nested(resource_fields_plane),
	'available' : fields.Integer
}

resource_fields_client = {
	'id': fields.Integer,
	'name' : fields.String,
	'mail' : fields.String,
	'nationality' : fields.String,
	'tickets' : fields.Nested(resource_fields)
}

class Ticket(Resource):
	@marshal_with(resource_fields)
	def get(self, Ticket_id):
		result = Flight.query.filter_by(id=Ticket_id).first()
		if not result:
			abort(404, message="Could not find Ticket with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, Ticket_id):
		args = Ticket_put_args.parse_args()
		result = Flight.query.filter_by(id=Ticket_id).first()
		if result:
			abort(409, message="Ticket id taken...")

		Ticket = Flight(id=Ticket_id, date_entree_api=args['date_entree_api'], reservation=args['reservation'], code_depart=args['code_depart'], code_destination=args['code_destination'], prix=args['prix'], name=args['name'])
		db.session.add(Ticket)
		db.session.commit()
		return Ticket, 201

	@marshal_with(resource_fields)
	def patch(self, Ticket_id):
		args = Ticket_update_args.parse_args()
		result = Flight.query.filter_by(id=Ticket_id).first()
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
		result = Flight.query.filter_by(id=Ticket_id).all()
		if not result:
			abort(404, message="Could not find Ticket with that id")
		return result
	

class Find_Ticket_by_date_dep(Resource):
	@marshal_with(resource_fields)
	def get(self, date):
		result = Flight.query.filter_by(date_departure=date).all()
		if not result:
			abort(404, message="Could not find Ticket with that departure date")
		return result

class Find_Ticket_by_date_arr(Resource):
	@marshal_with(resource_fields)
	def get(self, date):
		result = Flight.query.filter_by(date_arrival=date).all()
		if not result:
			abort(404, message="Could not find Ticket with that arrival date")
		return result

class Find_Ticket_by_max_price(Resource):
	@marshal_with(resource_fields)
	def get(self, price):
		result = Flight.query.filter_by(prix = price).all()
		if not result:
			abort(404, message="Could not find Ticket with that arrival date")
		return result


class All_Ticket(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = Flight.query.filter_by().all()
		if not result:
			abort(404, message="Could not find No Ticket")
		return result

class All_Client(Resource):
	@marshal_with(resource_fields_client)
	def get(self):
		result = Client.query.filter_by().all()
		if not result:
			abort(404, message="Could not find No Ticket")
		return result

class Find_client_by_mail(Resource):
	@marshal_with(resource_fields_client)
	def get(self, mail):
		result = Client.query.filter_by(mail=mail).all()
		if not result:
			abort(404, message="Could not find any client linkj to that mail")
		return result

class Find_Ticket_by_date(Resource):
	@marshal_with(resource_fields)
	def get(self, date):
		result = Flight.query.filter_by(date=date).all()
		if not result:
			abort(404, message="Could not find Ticket with that date")
		return result

class Find_Ticket_by_code(Resource):
	@marshal_with(resource_fields)
	def get(self, code):
		result = Flight.query.filter_by(code=code).all()
		if not result:
			abort(404, message="Could not find Ticket with that date")
		return result

class Add_Client(Resource):
	@marshal_with(resource_fields_client)
	def post(self):
		args = Client_put_args.parse_args()
		client = Client(id= 1,name=args['name'], mail=args['mail'],nationality=args['nationality'])
		db.session.add(client)
		db.session.commit()
		return client, 201

class Book(Resource):
	@marshal_with(resource_fields)
	def get(self, code, id):
		flight = Flight.query.filter_by(code=code).first()
		client = Client.query.filter_by(mail=mail).first()
		client.tickets.append(flight)
		db.session.commit()


api.add_resource(All_Ticket, "/tickets")
api.add_resource(All_Client, "/clients")
api.add_resource(Book, "/book/<string:code>?<string:id>")
api.add_resource(Add_Client, "/clients/add")
api.add_resource(Find_Ticket_by_date, "/tickets/date/<string:date>")
api.add_resource(Find_Ticket_by_code, "/tickets/code/<string:code>")
api.add_resource(Find_client_by_mail, "/clients/<string:mail>")


if __name__ == "__main__":
	app.run(debug=True)