import DB
from App import auth

from flask_restful import Resource
from flask import request

class Users(Resource):

    @auth.required
    def get(self):
        return [u.dict() for u in DB.User.query.all()]

    @auth.requires_role('admin')
    def post(self):
        data = request.get_json()
        if not ('name' in data and 'username' in data and 'email' in data and 'password' in data):
            return {'error': 'missing required information'}
        u = DB.User(data['name'], data['username'], data['email'], data['password'])
        DB.DB.session.add(u)
        DB.DB.session.commit()
        return u.dict()

class User(Resource):
    @auth.required
    def get(self, id):
        if 'admin' in g.user.roles:
            return g.user.full()
        return DB.User.query.get(id).dict()

    @auth.required
    def patch(self):
        data = request.get_json()

        # TODO Allow admin to do some changes
        if 'admin' in g.user.roles:
            return DB.query.get(data['id'])

        # Prohibit others from changing profile
        if g.user.id != data['id']:
            return {'error': 'Unauthorized'}

        # TODO Allow user to modify his/her profile
        return g.user.dict()
