from extensions import db


class City(db.Model):
    """ This class represents a City"""

    __tablename__ = 'cities'

    id = db.Column(db.INTEGER(), autoincrement=True, primary_key=True)
    name = db.Column(db.VARCHAR(), nullable=False, unique=True)