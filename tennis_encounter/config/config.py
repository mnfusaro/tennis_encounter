import os


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'nottomuchsecret123'
    )

    LOG_FILENAME = './log.txt'

    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }

    def __init__(self, exclude=[]):
        self.exclude = exclude
        variables = self.get_class_variables()
        self.validate_variables(variables)

    def validate_variables(self, variables):
        """Validate that all the variables are set
        You can exclude a variable validation by using the exclude list"""
        for key, value in variables.items():
            if isinstance(value, dict):
                self.validate_variables(value)
            if value is None and key not in self.exclude:
                raise ValueError(f'Value not provided for variable: {key}')

    def get_class_variables(self):
        """Obtain a dict with the config variables and their values"""
        return {attr: getattr(self, attr) for attr in dir(self)
                if not callable(getattr(self, attr)) and not attr.startswith('__')}


class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = 0
    TESTING = False
    DEVELOPMENT = False
    FLASK_ENV = 'production'

    # SQLAlchemy
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    }


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1
    TESTING = False
    DEVELOPMENT = True
    FLASK_ENV = 'development'

    # SQLAlchemy
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'secret')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'tennis_encounter_db')
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class StagingConfig(ProductionConfig):
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }


class TestingConfig(DevelopmentConfig):
    TESTING = True
    TESTDB_PATH = os.getcwd()+"test_db.sqlite"
    TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI
