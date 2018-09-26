from flask import Flask, request, jsonify, session, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from os import environ
from jinja2 import StrictUndefined
from model import db, Point, Team, User
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = environ['FLASK_SECRET_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


########################################################################################################################
# Page


@app.route('/')
def index():
    """Homepage."""

    team_scores = tally_up_team_points_into_dict()

    return render_template("index.html", team_scores=team_scores)


def tally_up_team_points_into_dict():

    user_point_counter = {}
    team_point_counter = {}

    points = Point.query.all()

    for point in points:
        user_point_counter[point.user] = user_point_counter.get(point.user, 0) + 1

    for key in user_point_counter:
        team_point_counter[key.team_id] = team_point_counter.get(key.team_id, 0) + user_point_counter.get(key)

    return team_point_counter




########################################################################################################################
# Main Function


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///voteinfo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
