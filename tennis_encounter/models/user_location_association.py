from extensions import db

# association_table = db.Table('user_location_association', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('location_id', db.Integer, db.ForeignKey('locations.id'))
# )


class UserLocationsAssociation(db.Model.metadata):
    """ This class represents a association between users and locations"""

    __tablename__ = 'user_location_association'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id')),
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
