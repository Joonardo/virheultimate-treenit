from flask import Flask

app = Flask(__name__)
app.config.from_object('config_dev')

from App import routes
from App import auth
