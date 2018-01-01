from flask_restful import Api

from App import app
from .event import Event, Events
from .user import User, Users
from .attend import Attend
from .roles import Roles

api = Api(app)

api.add_resource(User, '/api/users/<id>')
api.add_resource(Users, '/api/users')

api.add_resource(Roles, '/api/users/<id>/roles')

api.add_resource(Event, '/api/events/<id>')
api.add_resource(Events, '/api/events')

api.add_resource(Attend, '/api/events/<event_id>/attend')
