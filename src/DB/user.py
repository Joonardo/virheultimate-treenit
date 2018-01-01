from DB import DB

from App import app

from itsdangerous import (TimedJSONWebSignatureSerializer as Ser,
                            BadSignature, SignatureExpired)

serializer = Ser(app.config['SECRET_KEY'], expires_in=900)

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
        self.password_hash = pw # TODO hash it
        self.m_roles = "USER"

    @property
    def roles(self):
        return self.m_roles.split(',')

    @roles.setter
    def roles(self, nroles):
        if all(not ',' in r for r in nroles):
            return
        self.m_roles = ','.join(nroles)

    def add_role(self, role):
        if "," in role:
            return
        self.roles = self.roles + [role]

    def authorize(self, pw):
        # TODO hash it
        return pw == self.password_hash

    def generate_auth_token(self):
        return serializer.dumps({'id': self.id}).decode()

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
            'roles': self.roles # TODO remove in production
        }
