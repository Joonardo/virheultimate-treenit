from flask_restful import Resource

import DB

class Events(Resource):
    def get(self):
        return [ev.dict() for ev in DB.Event.query.all()]

    def post(self):
        c = len(DB.Event.query.all())
        ev = DB.Event('Whoo', 'This is #{:d} event.'.format(c))
        DB.DB.session.add(ev)
        DB.DB.session.commit()
        return ev.dict()

class Event(Resource):
    def get(self, id):
        return DB.Event.query.get(id).dict()
