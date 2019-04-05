from sqlalchemy import Column, Text, Integer

from SDMPDS import db


class Question(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    date = Column(Text, nullable=False)
    device_id = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    coordinates = Column(Text, nullable=False)
    question = Column(Text, nullable=False)

    def __repr__(self):
        return '<Question {}>'.format(self.id)

    def __str__(self):
        return '<Question {}>\nData utworzenia: {}\nID urządzenia: {}\n\
                koordynaty: {}\nname: {}\nquestion' \
            .format(
            self.id,
            self.date,
            self.device_id,
            self.coordinates,
            self.name,
            self.question
        )
