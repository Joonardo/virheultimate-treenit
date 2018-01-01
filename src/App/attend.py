from flask_restful import Resource
from flask import g

from App import auth
import DB

class Attend(Resource):
    @auth.required
    def post(self, event_id):
        ev = DB.Event.query.get(event_id)
        ev.status_in(g.user)
        DB.DB.session.commit()
        return ev.dict()

    @auth.required
    def delete(self, event_id):
        ev = DB.Event.query.get(event_id)
        ev.status_out(g.user)
        DB.DB.session.commit()
        return ev.dict()
