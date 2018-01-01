import DB
from flask_restful import Resource
from flask import request

class Users(Resource):
    def get(self):
        return [u.dict() for u in DB.User.query.all()]

    def post(self):
        # TODO some authorization
        # perhaps add roles to user and allow only admin to
        # use this endpoint
        data = request.get_json()
        if not ('name' in data and 'username' in data and 'email' in data and 'password' in data):
            return {'error': 'missing required information'}
        u = DB.User(data['name'], data['username'], data['email'], data['password'])
        DB.DB.session.add(u)
        DB.DB.session.commit()
        return u.dict()

class User(Resource):
    def get(self, id):
        return DB.User.query.get(id).dict()
