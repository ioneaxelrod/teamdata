from flask_sqlalchemy import SQLAlchemy
from os import environ

db = SQLAlchemy()

def connect_to_db(app):
    """Connect the database to our Flask app.
    :param app: Flask application
    :return None
    """

    # Configure to use our MySQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
