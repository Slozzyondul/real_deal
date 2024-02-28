from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load configuration from a config file
app.config.from_pyfile('config.cfg')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Test model
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)

# Define Students model
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(40))
    email = db.Column(db.String(50))
    date = db.Column(db.DateTime)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()