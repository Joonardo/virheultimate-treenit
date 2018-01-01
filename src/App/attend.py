from flask_restful import Resource

class Attend(Resource):
    def post(self, event_id):
        # TODO add current user to event
        pass

    def delete(self, event_id):
        # TODO remove current user from event
        pass
