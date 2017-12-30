from flask_restful import Api

from App import app
from .event import Event, Events
from .user import User

api = Api(app)

api.add_resource(User, '/api/users')
api.add_resource(Event, '/api/events/<id>')
api.add_resource(Events, '/api/events')
