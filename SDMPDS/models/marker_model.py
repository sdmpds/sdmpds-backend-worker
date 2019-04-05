from sqlalchemy import Column, Text, Integer

from SDMPDS import db


class Marker(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    date = Column(Text, nullable=False)
    device_id = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    recognized = Column(Integer, nullable=True)
    coordinates = Column(Text, nullable=False)
    img_src = Column(Text, nullable=False, unique=True)
    status = Column(Text, nullable=True)

    def __repr__(self):
        return '<Markers {}>'.format(self.id)

    def __str__(self):
        return '<Markers {}>\nData utworzenia zdjęcia: {}\nID urządzenia: {}\nRozpoznanie: {}\n\
                koordynaty: {}\nMiejsce zapisu: {}\nStatus: {}\nname: {}' \
            .format(
            self.id,
            self.date,
            self.device_id,
            self.recognized,
            self.coordinates,
            self.img_src,
            self.status,
            self.name
        )
