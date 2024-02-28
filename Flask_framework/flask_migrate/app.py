'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home/solo/Desktop/Flask_framework/flask_migrate/database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

if __name__== '__main__':
    app.run(debug=True)
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home/solo/Desktop/Flask_framework/flask_migrate/database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)


if __name__ == '__main__':
    manager.run()
    try:
        db.create_all()  # Create the database tables
        app.run(debug=True)
    except Exception as e:
        print("Error occurred during application initialization:", e)
