from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class BilletModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_entree_api = db.Column(db.String, nullable=False)
	reservation = db.Column(db.Boolean, nullable=False)
	code_depart = db.Column(db.String(3), nullable=False)
	code_destination = db.Column(db.String(3), nullable=False)
	prix = db.Column(db.Integer, nullable=False)
	name = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f("Billet (id = {self.id}, date_entree_api = {self.date_entree_api}, reservation = {self.reservation}, code_depart{self.code_depart}, code_destination = {self.code_destination}, prix = {self.prix}, name = {self.name})")

db.create_all()

billet_put_args = reqparse.RequestParser()
billet_put_args.add_argument("id", type=int, help="ID nombre unique pour un billet", required=True)
billet_put_args.add_argument("date_entree_api", type=str, help="Date de création dans l'api", required=True)
billet_put_args.add_argument("reservation", type=bool, help="Savoir si un billet est reserve ou pas", required=True)
billet_put_args.add_argument("code_depart", type=str, help="Abréviation de l'aéroport de depart", required=True)
billet_put_args.add_argument("code_destination", type=str, help="Abréviation de l'aéroport d'arrive", required=True)
billet_put_args.add_argument("prix", type=int, help="Prix du billet en euro", required=True)
billet_put_args.add_argument("name", type=str, help="Nom du propriétaire du billet", required=True)


billet_update_args = reqparse.RequestParser()
billet_put_args.add_argument("id", type=int, help="ID nombre unique pour un billet", required=True)
billet_put_args.add_argument("date_entree_api", type=str, help="Date de création dans l'api", required=True)
billet_put_args.add_argument("reservation", type=bool, help="Savoir si un billet est reserve ou pas", required=True)
billet_put_args.add_argument("code_depart", type=str, help="Abréviation de l'aéroport de depart", required=True)
billet_put_args.add_argument("code_destination", type=str, help="Abréviation de l'aéroport d'arrive", required=True)
billet_put_args.add_argument("prix", type=int, help="Prix du billet en euro", required=True)
billet_put_args.add_argument("name", type=str, help="Nom du propriétaire du billet", required=True)

resource_fields = {
	'id': fields.Integer,
	'date_entree_api': fields.String,
	'reservation': fields.Boolean,
	'code_depart': fields.String,
	'code_destination': fields.String,
	'prix': fields.Integer,
	'name': fields.String,
}

class Billet(Resource):
	@marshal_with(resource_fields)
	def get(self, billet_id):
		result = BilletModel.query.filter_by(id=billet_id).first()
		if not result:
			abort(404, message="Could not find billet with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, billet_id):
		args = billet_put_args.parse_args()
		result = BilletModel.query.filter_by(id=billet_id).first()
		if result:
			abort(409, message="Billet id taken...")

		billet = BilletModel(id=billet_id, date_entree_api=args['date_entree_api'], reservation=args['reservation'], code_depart=args['code_depart'], code_destination=args['code_destination'], prix=args['prix'], name=args['name'])
		db.session.add(billet)
		db.session.commit()
		return billet, 201

	@marshal_with(resource_fields)
	def patch(self, billet_id):
		args = billet_update_args.parse_args()
		result = BilletModel.query.filter_by(id=billet_id).first()
		if not result:
			abort(404, message="Billet doesn't exist, cannot update")

		if args['id']:
			result.name = args['id']
		if args['date_entree_api']:
			result.views = args['date_entree_api']
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


	def delete(self, billet_id):
		abort_if_billet_id_doesnt_exist(billet_id)
		del billets[billet_id]
		return '', 204


api.add_resource(Billet, "/billet/<int:billet_id>")

if __name__ == "__main__":
	app.run(debug=True)