from extensions import db
from user_location_association import UserLocationsAssociation

association_table = db.Table('user_location_association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('locations.id'))
)


class Location(db.Model):
    """ This class represents a City"""

    __tablename__ = 'locations'

    id = db.Column(db.INTEGER(), autoincrement=True, primary_key=True)
    city_id = db.Column(db.INTEGER(), db.ForeignKey('cities.id'))
    state_id = db.Column(db.INTEGER(), db.ForeignKey('states.id'))
    users = db.relationship(
        "User",
        secondary=UserLocationsAssociation,
        back_populates="locations")