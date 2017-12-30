from DB import DB

class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(30), nullable=False)
    username = DB.Column(DB.String(30), nullable=True)
    email = DB.Column(DB.String(30), nullable=False)
    password_hash = DB.Column(DB.String(50), nullable=False)
