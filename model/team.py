from .db import db


class Team(db.Model):

    __tablename__ = 'team'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(45))
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
