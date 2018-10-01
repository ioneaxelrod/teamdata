from .db import db
from .user import User


class Point(db.Model):

    __tablename__ = 'points'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    points = db.Column(db.Integer)
    reason = db.Column(db.String(45))
    date_created = db.Column(db.DateTime)

    user = db.relationship("User", backref="points")
