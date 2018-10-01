from .db import db
from .team import Team


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(45))
    team_id = db.Column(db.Integer, db.ForeignKey(Team.id))
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)

    team = db.relationship("Team", backref="users")
