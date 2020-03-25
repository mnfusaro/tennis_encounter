"""
This module is used for DB migrations.
"""
import fileinput
import os
import sys

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Command

"""
IMPORTANT: You must import the models in the correct order,
otherwhise the db upgrade command will fail.
"""
from models.cities import City
from models.states import State
from models.locations import Location
from models.users import User, GameLevel
from models.user_location_association import association_table
from extensions import db


config = {
    "production": "config.config.ProductionConfig",
    "development": "config.config.DevelopmentConfig",
    "staging": "config.config.StagingConfig",
    "testing": "config.config.TestingConfig"
}

app = Flask(__name__)
config_name = os.environ['APPLICATION_ENV']
app.config.from_object(config[config_name])

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class FixUUID(Command):
    """Replace the custom GUID by postgres UUID in the migration version files
    """
    def run(self):
        # Get migration version files from migrations folder
        migrations_path = 'migrations/versions'
        migration_files = []
        for (dirpath, dirnames, filenames) in os.walk(migrations_path):
            migration_files.extend([f for f in filenames if f.endswith('.py')])
            break

        postgres_import = 'from sqlalchemy.dialects import postgresql'
        # Replace the GUID definition by the postgres UUID definition
        for migration_file in migration_files:
            searchExp = 'utils.db.GUID()'
            replaceExp = 'postgresql.UUID(as_uuid=True)'
            for line in fileinput.input(f'{migrations_path}/{migration_file}',
                                        inplace=True):
                if fileinput.isfirstline():
                    if postgres_import not in line:
                        # Insert the import sentece for postgresql
                        line = line.replace(line, f'{postgres_import}\n{line}')
                elif searchExp in line:
                    line = line.replace(searchExp, replaceExp)
                elif postgres_import in line:
                    # Skip the import sentence if it was already there
                    continue
                sys.stdout.write(line)


manager.add_command('fixuuid', FixUUID)


if __name__ == '__main__':
    manager.run()
