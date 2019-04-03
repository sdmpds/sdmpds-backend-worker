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
    date = Column(Text, nullable=False)
    name = Column(Text, nullable=False, unique=True)
    recognized = Column(Integer, nullable=True)
    coordinates = Column(Text, nullable=False)
    img_src = Column(Text, nullable=False, unique=True)
    status = Column(Text, nullable=True)

    def __repr__(self):
        return '<Image {}>'.format(self.name)

    def __str__(self):
        return '<Image {}>\ndate: {}\nname: {}\ncolor: {}\nrecognized: {}\n\
        coordinates: {}\nimg_src: {}\nstatus: {}'.format(self.name, self.color,
                                                         self.recognized, self.coordinates, 
                                                         self.img_src, self.status)
