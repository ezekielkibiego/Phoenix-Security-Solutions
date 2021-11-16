from app import create_app, db
from app.models import User
from flask_script import Manager, Server


# Creating app instance
app = create_app('development')

manager = Manager(app)
manager.add_command('server', Server)

@manager.shell
def make_shell_context():
  return dict(app = app, db = db, User = User)