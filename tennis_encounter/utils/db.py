from datetime import datetime
import logging

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.sql import func
from extensions import db
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid


class BaseDBMethods():
    """Base class for DB methods"""

    @classmethod
    def get_one(cls, model_class, **kwargs):
        """Get one instance of a model from the DB

        Arguments
        ---------
            model_class : class
            kwargs : dict

        Returns
        -------
            a tuple with:
            - a boolean indicating whether the action was successful or not
            - either the object or an error message if the action failed
        """
        try:
            model = model_class.query.filter_by(**kwargs).one()
            model.id = str(model.id)
            return True, model
        except MultipleResultsFound:
            error = 'DB_MODEL_ASK_ONE_GET_MORE_ERROR'
            logging.exception(error)
            return False, error
        except NoResultFound:
            error = 'DB_MODEL_NOT_FOUND_ERROR'
            logging.exception(error)
            return False, error
        except Exception:
            error = 'DB_MODEL_GET_ONE_ERROR'
            logging.exception(error)
            return False, error

    @classmethod
    def get_many(cls, model_class, **kwargs):
        """Get many instances of a model from the DB

        Arguments
        ---------
            model_class : class

        Returns
        -------
            a tuple with:
            - a boolean indicating whether the action was successful or not
            - either the list of objects or an error message if the
              action failed
        """
        try:
            models = model_class.query.filter_by(**kwargs).all()
            return True, models
        except Exception:
            error = 'DB_MODEL_GET_MANY_ERROR'
            logging.exception(error)
            return False, error

    @classmethod
    def get_many_in_list(cls, model_class, field, filter_list):
        """Get many instances of a model within a list of values from the DB

        Arguments
        ---------
            model_class : class
            field : string
            filter_list : list

        Returns
        -------
            a tuple with:
            - a boolean indicating whether the action was successful or not
            - either the lisft of objects or an error message if the
              action failed
        """
        try:
            models = model_class.query.filter(
                getattr(model_class, field).in_(filter_list)).all()
            return True, models
        except Exception:
            error = 'DB_MODEL_GET_MANY_IN_LIST_ERROR'
            logging.exception(error)
            return False, error

    @classmethod
    def save(cls, model, update=False):
        """Save a model to the DB

        Arguments
        ---------
            model : model
            update : boolean

        Returns
        -------
            a tuple with:
            - a boolean indicating whether the action was successful or not
            - either the object or an error message if the action failed
        """
        try:
            if not update:
                db.session.add(model)
            db.session.commit() # TODO chequear esto
            return True, model
        except Exception:
            db.session.rollback()
            error = 'DB_MODEL_SAVE_ERROR'
            logging.exception(error)
            return False, error

    @classmethod
    def save_many(cls, records):
        """Save many records to the DB

        Arguments
        ---------
            records : list

        Returns
        -------
            a tuple with:
            - a boolean indicating whether the action was successful or not
            - either a list of objects or an error message if the action failed
        """
        try:
            db.session.add_all(records)
            db.session.commit()
            return True, records
        except Exception:
            db.session.rollback()
            error = 'DB_MODEL_SAVE_MANY_ERROR'
            logging.exception(error)
            return False, error

    @classmethod
    def update(cls, model, **kwargs):
        """Update a model in the DB

        Arguments
        ---------
            model : model
            kwargs : dict

        Returns
        -------
            a tuple with:
            - a boolean indicating whether the action was successful or not
            - either the object or an error message if the action failed
        """
        try:
            for key, value in kwargs.items():
                setattr(model, key, value)
            db.session.commit()
            return True, model
        except Exception:
            db.session.rollback()
            error = 'DB_MODEL_UPDATE_ERROR'
            logging.exception(error)
            return False, error

    @classmethod
    def delete(cls, model):
        """Delete a model from the DB

        Arguments
        ---------
            model: model

        Returns
        -------
            a tuple with:
            - a boolean indicating whether the action was successful or not
            - either None or an error message if the action failed
        """
        try:
            db.session.delete(model)
            db.session.commit()
            return True, None
        except Exception:
            db.session.rollback()
            error = 'DB_MODEL_DELETE_ERROR'
            logging.exception(error)
            return False, error

    @classmethod
    def to_dict(cls, model):
        """Serialize model into dict

        Arguments
        ---------
            model : model

        Returns
        -------
            a dict from the model provided
        """
        def getattr_name(obj):
            if isinstance(obj, str):
                return obj
            return getattr(obj, 'name')

        convert = {
            'DATETIME': datetime.isoformat,
            'UUID': str,
            'GUID': str,
            'ENUM': getattr_name,
        }
        model_dict = {}
        for column in model.__class__.__table__.columns:
            if column.name.startswith('_'):
                continue
            value = getattr(model, column.name)
            current_type = column.type.__class__.__name__.upper()
            if current_type in convert.keys() and value is not None:
                try:
                    model_dict[column.name] = convert[current_type](value)
                except Exception:
                    model_dict[column.name] = (
                        'Error: Failed to covert using ',
                        convert[column.type]
                    )
            elif value is None:
                model_dict[column.name] = ''
            else:
                model_dict[column.name] = value
        return model_dict

    @classmethod
    def get_aggregate_sum(cls, model_class, field, *args, **kwargs):
        try:
            aggr = db.session.query(func.sum(getattr(model_class, field))).filter(*args, **kwargs).first()  # noqa
            value = aggr[0] if aggr[0] else 0
            return value
        except Exception:
            error = 'DB_MODEL_AGGREGATION_ERROR'
            logging.exception(error)
            db.session.rollback()
            return None


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
