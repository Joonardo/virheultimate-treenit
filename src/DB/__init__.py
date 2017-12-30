from flask_sqlalchemy import SQLAlchemy
from App import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

DB = SQLAlchemy(app)

from .user import User
from .event import Event

DB.create_all()
