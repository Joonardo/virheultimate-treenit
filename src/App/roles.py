from flask_restful import Resource
from flask import request

from App import auth
import DB

class Roles(Resource):
    @auth.requires_role('admin')
    def get(self, id):
        return DB.User.query.get(id).roles

    @auth.requires_role('admin')
    def post(self, id):
        data = request.get_json()
        DB.User.query.get(id).add_role(data['role'])
        DB.DB.session.commit()
        return DB.User.query.get(id).dict()

    @auth.requires_role('admin')
    def delete(self, id):
        data = request.get_json()
        DB.User.query.get(id).remove_role(data['role'])
        DB.DB.session.commit()
        return DB.User.query.get(id).dict()
