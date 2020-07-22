from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from fixtures import seed_db
from model import *

migrate = Migrate(app, db)
manager = Manager(app)


@app.cli.command("seed", help="Seed DB with test data")
def seed_db_cmd():
    seed_db()

manager.add_command('seed', seed_db_cmd())
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()