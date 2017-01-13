# package imports
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# relative imports
from api_1_0.app import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
