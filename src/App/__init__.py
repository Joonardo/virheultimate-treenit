from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty123'

from App import routes
from App import auth
