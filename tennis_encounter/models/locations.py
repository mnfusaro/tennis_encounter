from extensions import db
from models.user_location_association import association_table


class Location(db.Model):
    """ This class represents a City"""

    __tablename__ = 'locations'

    id = db.Column(db.INTEGER(), autoincrement=True, primary_key=True)
    city_id = db.Column(db.INTEGER(), db.ForeignKey('cities.id'))
    state_id = db.Column(db.INTEGER(), db.ForeignKey('states.id'))
    users = db.relationship(
        "User",
        secondary=association_table,
        back_populates="locations")