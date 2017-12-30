from flask_restful import Resource

from DB import DB

class Events(Resource):
    def get(self):
        return {'ev': 'all'}

class Event(Resource):
    def get(self, id):
        return {'ev': id}
