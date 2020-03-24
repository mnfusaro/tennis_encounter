from enum import Enum
from sqlalchemy_utils import ChoiceType
from sqlalchemy.dialects import postgresql
from utils.db import GUID

from extensions import db
from user_location_association import UserLocationsAssociation


class GameLevel(Enum):
    """Game level enum"""
    beginner = 1
    intermediate = 2
    advanced = 3


class User(db.Model):
    """ This class represents a User"""

    __tablename__ = 'users'

    id = db.Column(GUID(), primary_key=True)
    game_level = db.Column(ChoiceType(GameLevel, impl=db.Integer()))
    password = db.Column(db.LargeBinary(60), nullable=False)
    places = db.Column(postgresql.ARRAY(db.INTEGER()))
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.SmallInteger, nullable=False)
    description = db.Column(db.Text)
    locations = db.relationship(
        "Location",
        secondary=UserLocationsAssociation,
        back_populates="users")

    #  card_enabled = db.Column(db.Boolean, index=True, nullable=False)
    # locations = db.Column(db.ARRAY(db.Integer), nullable=True)
