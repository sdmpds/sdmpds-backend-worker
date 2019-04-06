from quart import Quart
from flask_sqlalchemy import SQLAlchemy
import redis
import os

app = Quart(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/ServerDatabase.db'
db = SQLAlchemy(app)
# SR = redis.StrictRedis(host='localhost', port=6379)
# SR.execute_command('FLUSHDB')

url = os.getenv('REDISCLOUD_URL')
if url:
    SR = redis.Redis.from_url(url)
else:
    SR = redis.StrictRedis(host='localhost', port=6379)

import SDMPDS.controllers.root_controller
