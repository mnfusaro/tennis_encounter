from extensions import db
from utils.db import GUID

association_table = db.Table('user_location_associations', db.Model.metadata,
    db.Column('user_id', GUID(), db.ForeignKey('users.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('locations.id'))
)


# class UserLocationAssociation(db.Model.metadata):
#     """ This class represents a association between users and locations"""
#
#     __tablename__ = 'user_location_associations'
#
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id')),
#     location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
