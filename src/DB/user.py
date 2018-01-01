from DB import DB

class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(30), nullable=False)
    username = DB.Column(DB.String(30), nullable=True)
    email = DB.Column(DB.String(30), nullable=False)
    password_hash = DB.Column(DB.String(50), nullable=False)

    def __init__(self, rn, un, em, pw):
        self.name = rn
        self.username = un
        self.email = em
        self.password_hash = pw # TODO hash it

    def authorize(self, pw):
        # TODO hash it
        return pw == self.password_hash

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email
        }
