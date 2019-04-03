from quart import Quart
from flask_sqlalchemy import SQLAlchemy


app = Quart(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/ServerDatabase.db'
db = SQLAlchemy(app)

import SDMPDS.views
