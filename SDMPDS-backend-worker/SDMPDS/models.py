from SDMPDS import db
from sqlalchemy import Column, Text, Integer

class Users(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    login = Column(Text, nullable=False, unique=True)
    nazwa = Column(Text, nullable=False, default="Anonim")
    token = Column(Text, nullable=False, unique=True)
    data_utworzenia_tokenu = Column(Text, nullable=False)

    def __repr__(self):
        return '<ActiveUser %s>' % self.token

class Images(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    img_src = Column(Text, nullable=False, unique=True)
    data_modyfikacji = Column(Text, nullable=False)

    def __repr__(self):
        return '<Image %s>' % self.name

