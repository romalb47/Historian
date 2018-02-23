#!/usr/bin/env python3

from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
import json

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

MainClass = 0

class CurvesCollection(Resource):
	def get(self):
		data = MainClass.bdd.execute("SELECT idx FROM identifiant").fetchall()
		return data

	def post(self):
		pass


class Curves(Resource):
	def get(self, id):
		data = MainClass.bdd.execute("SELECT * FROM identifiant WHERE idx=?", (id,)).fetchall()
		return data

	def put(self, id):
		return {"msg": "Update user id {}".format(id)}

	def delete(self, id):
		return {"msg": "Delete user id {}".format(id)}


api.add_resource(CurvesCollection, '/curves')
api.add_resource(Curves, '/curves/<int:id>')
