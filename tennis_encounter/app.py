import importlib
import os
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from extensions import db
import logging
from logging.config import dictConfig
from flask import Flask, abort
from flask_restplus import Resource, Api


def create_app():
    config = {
        "production": "ProductionConfig",
        "development": "DevelopmentConfig",
        "staging": "StagingConfig",
        "testing": "TestingConfig"
    }
    api = Api()
    app = Flask(__name__)
    api.init_app(app, appversion='1.0', title='Tennis Encounter',
              description='An API to manage groups and people dates to play tennis.')

    config_name = os.environ['APPLICATION_ENV']
    config_module = importlib.import_module('config.config')
    config_class = getattr(config_module, config[config_name])
    app.config.from_object(config_class())

    dictConfig(config_class.LOGGING_CONFIG)

    db.init_app(app)

    @api.route('/index')
    class index(Resource):
        def get(self):
            try:
                db.engine.connect()
                return {'status': 'working'}

            except Exception as e:
                abort(500, e)
    return app


if __name__ == '__main__':
    app = create_app()
    logging.info("*** Starting Tennis Encounter API ***")
    app.run(host='0.0.0.0')