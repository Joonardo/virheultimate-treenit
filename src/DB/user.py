from DB import DB
from App import app

from itsdangerous import (TimedJSONWebSignatureSerializer as Ser,
                            BadSignature, SignatureExpired)
from passlib.hash import bcrypt

serializer = Ser(app.config['SECRET_KEY'], expires_in=9000)

class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(30), nullable=False)
    username = DB.Column(DB.String(30), nullable=True)
    email = DB.Column(DB.String(30), nullable=False, unique=True)
    password_hash = DB.Column(DB.String(50), nullable=False)
    m_roles = DB.Column(DB.Text)

    def __init__(self, rn, un, em, pw):
        self.name = rn
        self.username = un
        self.email = em
        self.password_hash = bcrypt.hash(pw)
        self.m_roles = "USER"

    @property
    def roles(self):
        return self.m_roles.split(',')

    @roles.setter
    def roles(self, nroles):
        if any(',' in r for r in nroles):
            return
        self.m_roles = ','.join(set(nroles))

    def remove_role(self, role):
        self.roles = [r for r in self.roles if r != role.upper()]

    def add_role(self, role):
        if "," in role:
            return
        self.roles = self.roles + [role.upper()]

    def authorize(self, pw):
        return bcrypt.verify(pw, self.password_hash)

    def generate_auth_token(self):
        return serializer.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = serializer.loads(token.encode())
            return User.query.get(data['id'])
        except SignatureExpired:
            return None
        except BadSignature:
            return None

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
        }

    def full(self):
        return {**(self.dict()), **{
            'roles': self.roles
        }}
