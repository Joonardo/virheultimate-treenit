from DB import DB
from flask_restful import Resource

class User(Resource):
    def get(self):
        return {'Hello': 'World'}