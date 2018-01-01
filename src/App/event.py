from flask_restful import Resource
from flask import request

import DB
from App import auth

class Events(Resource):
    @auth.required
    def get(self):
        return [ev.dict() for ev in DB.Event.query.all()]

    @auth.required
    def post(self):
        data = request.get_json()
        if not ('name' in data and 'description' in data):
            return {'error': 'missing required information'}
        ev = DB.Event(data['name'], data['description'])
        DB.DB.session.add(ev)
        DB.DB.session.commit()
        return ev.dict()

class Event(Resource):
    @auth.required
    def get(self, id):
        return DB.Event.query.get(id).dict()
