# package imports
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# relative imports
from api_1_0.app import app, db
from api_1_0.seeds import Seeder

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Add seed data to the db
@manager.option('-c', '--count', help='Quantity of records to seed')
def dbseed(count):
    count = int(count)
    Seeder.seed_users(count)
    Seeder.seed_call_actions(count)
    Seeder.seed_email_actions(count)
    Seeder.seed_event_actions(count)

if __name__ == '__main__':
    manager.run()
