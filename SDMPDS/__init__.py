from quart import Quart
from flask_sqlalchemy import SQLAlchemy
import redis


app = Quart(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/ServerDatabase.db'
db = SQLAlchemy(app)
SR = redis.StrictRedis(host='localhost', port=6379)
SR.execute_command('FLUSHDB')

import SDMPDS.controllers.root_controller
