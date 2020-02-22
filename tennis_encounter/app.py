import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app, appversion='1.0', title='Tennis Encounter',
          description='An API to manage groups and people dates to play tennis.')


@api.route('/index')
class index(Resource):
    def get(self):
        return {'status': 'working'}


if __name__ == '__main__':
    app.run()