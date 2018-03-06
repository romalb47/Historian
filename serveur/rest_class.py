#!/usr/bin/env python3

import os

from flask import Flask, request, send_from_directory, abort, jsonify, g, url_for
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
						  as Serializer, BadSignature, SignatureExpired)
						  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api = Api(app, prefix="/api/v1")

MainClass = 0


class CurvesCollection(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('start', dest='start', location='form', type=str, default="00/00/0000 00:00:00")

	def get(self):
		c = MainClass.bdd.execute("SELECT idx FROM history GROUP BY idx")
		data = []
		for i in c:
			data.append(i["idx"])
		return data

class Curves(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('start', dest='start', location='form', type=str, default="1970-01-01T00:00:00")
		self.reqparse.add_argument('end', dest='end', location='form', type=str, default="2099-01-01T00:00:00")

	def get(self, idc):
		args = self.reqparse.parse_args()
		print(args)
		c = MainClass.bdd.execute("SELECT name, format FROM identifiant WHERE idx=?", (idc,)).fetchone()
		data_global = {"idx": idc, "name":str(c["name"]), "data":[], "format": str(c["format"])}
		data = []
		c = MainClass.bdd.execute("SELECT data, time FROM history WHERE idx=? AND ( time<DATETIME(?) AND time>DATETIME(?) )", (idc, args["end"], args["start"]))
		for i in c:
			data.append({"data":i["data"], "time":i["time"]})
		data_global["data"] = data
		return data_global

	def delete(self, id):
		return {"msg": "Delete user id {}".format(id)}
		
class EventsCollection(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('x-token', type=str, location='headers', required=True)

	def get(self):
		c = MainClass.bdd.execute("SELECT ide FROM event GROUP BY ide")
		data = []
		for i in c:
			data.append(i["ide"])
		return data

class Events(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('x-token', type=str, location='headers', required=True)

	def get(self, ide):
		c = MainClass.bdd.execute("SELECT event_text, time FROM event WHERE ide=?", (ide,))
		data_global = {"ide": ide, "name":"ID-"+str(ide), "data":[]}
		data = []
		for i in c:
			data.append({"text":i["event_text"], "time":i["time"]})
		data_global["data"] = data
		return data_global

	def delete(self, id):
		return {"msg": "Delete user id {}".format(id)}

class DatasetsCollection(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('x-token', type=str, location='headers', required=True)

	def get(self):
		c = MainClass.bdd.execute("SELECT idd FROM dataset GROUP BY idd")
		data = []
		for i in c:
			data.append(i["idd"])
		return data

class Datasets(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('x-token', type=str, location='headers', required=True)

	def get(self, idd):
		c = MainClass.bdd.execute("SELECT type, ident FROM dataset WHERE idd=?", (idd,))
		data_global = {"idd": idd, "data":[]}
		data = []
		for i in c:
			data.append({"type":i["type"], "ident":i["ident"]})
		data_global["data"] = data
		return data_global

	def delete(self, id):
		return {"msg": "Delete user id {}".format(id)}

class Users(Resource):
	def get(self, id):
		c = MainClass.bdd.execute("SELECT * FROM identifiant WHERE idx=?", (id,))
		return data

	def put(self, id):
		return {"msg": "Update user id {}".format(id)}

	def delete(self, id):
		return {"msg": "Delete user id {}".format(id)}
		
class UsersLogin(Resource):
	def get(self, id):
		c = MainClass.bdd.execute("SELECT * FROM identifiant WHERE idx=?", (id,))
		return data

	def put(self, id):
		return {"msg": "Update user id {}".format(id)}

	def delete(self, id):
		return {"msg": "Delete user id {}".format(id)}

api.add_resource(CurvesCollection, '/curves')
api.add_resource(Curves, '/curves/<int:idc>/data')

api.add_resource(EventsCollection, '/events')
api.add_resource(Events, '/events/<int:ide>/data')

api.add_resource(DatasetsCollection, '/datasets')
api.add_resource(Datasets, '/datasets/<int:idd>/data')

api.add_resource(Users, '/users')
api.add_resource(UsersLogin, '/users/auth')
