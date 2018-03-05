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
		self.reqparse.add_argument('x-token', type=str, location='headers', required=True)

	def get(self):
		data = self.reqparse.parse_args()
		if data['x-token'] == "SECRET":
			return("200 Success")
		data = MainClass.bdd.execute("SELECT idx FROM identifiant").fetchall()
		return data

	def post(self):
		pass
		

class Curves(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('x-token', type=str, location='headers', required=True)

	def get(self, id):
		data = MainClass.bdd.execute("SELECT * FROM identifiant WHERE idx=?", (id,)).fetchall()
		return data

	def put(self, id):
		return {"msg": "Update user id {}".format(id)}

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
		
		
class Data(Resource):
	def get(self, idx):
		c = MainClass.bdd.execute("SELECT data, time FROM history WHERE idx=?", (idx,))
		time = []
		value = []
		for i in c:
			time.append(i["time"])
			value.append(i["data"])
		return {"data": value, "time": time}


api.add_resource(CurvesCollection, '/curves')
api.add_resource(Curves, '/curves/<int:id>')
api.add_resource(Data, '/data/<int:idx>')
