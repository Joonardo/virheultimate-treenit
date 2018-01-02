import DB
from App import auth

from flask_restful import Resource
from flask import request, g

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
    def patch(self, id):
        data = request.get_json()

        # Allow admin to do some changes
        if 'ADMIN' in g.user.roles:
            user = DB.User.query.get(id)

            if not user:
                return {'error': 'invalid user id'}

            user.modify(data)

            DB.DB.session.commit()
            return user.full()

        # Prohibit others from changing profile
        if g.user.id != int(id):
            return {'error': 'Unauthorized change'}

        # Allow user to modify his/her profile

        # Prohibit user from changing some fields
        denied_keys = ['roles']
        for key in denied_keys:
            if key in data:
                del data[key]

        g.user.modify(data)

        DB.DB.session.commit()
        return g.user.dict()
