from extensions import db


class State(db.Model):
    """ This class represents a State"""

    __tablename__ = 'states'

    id = db.Column(db.INTEGER(), autoincrement=True, primary_key=True)
    name = db.Column(db.VARCHAR(), nullable=False, unique=True)