from flask_restful import Resource

from DB import DB

class Events(Resource):
    def get(self):
        # TODO list all events
        return {'ev': 'all'}

class Event(Resource):
    def get(self, id):
        return {'ev': id}

    def post(self):
        # TODO add new events
        pass
