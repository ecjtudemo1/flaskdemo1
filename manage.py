from app import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, socketio
app.config['SECRET_KEY'] = '44694a31fa044b51872d67344966a742'
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('run', socketio.run(app=app, host='127.0.0.1', port=5000))
if __name__ == "__main__":
    manager.run()