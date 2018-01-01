from flask_restful import Resource
from flask import request

import DB

class Events(Resource):
    def get(self):
        return [ev.dict() for ev in DB.Event.query.all()]

    def post(self):
        data = request.get_json()
        if not ('name' in data and 'description' in data):
            return {'error': 'missing required information'}
        ev = DB.Event(data['name'], data['description'])
        DB.DB.session.add(ev)
        DB.DB.session.commit()
        return ev.dict()

class Event(Resource):
    def get(self, id):
        return DB.Event.query.get(id).dict()
