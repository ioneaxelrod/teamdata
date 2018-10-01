from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from os import environ
from jinja2 import StrictUndefined
from model import db, Point, Team


application = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
application.secret_key = environ['FLASK_SECRET_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
application.jinja_env.undefined = StrictUndefined

# Configure to use our MySQL database
db.app = application
db.init_app(application)
application.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


########################################################################################################################
# Page


@application.route('/')
def index():
    """Homepage."""

    scores = tally_up_team_points_into_dict()
    teams = Team.query.all()
    teams_scores = [(team.name, scores.get(team.id)) for team in teams]

    return render_template("index.html", teams_scores=teams_scores)


def tally_up_team_points_into_dict():

    user_point_counter = {}
    team_point_counter = {}

    points = Point.query.all()

    for point in points:
        user_point_counter[point.user] = user_point_counter.get(point.user, 0) + point.points

    for key in user_point_counter:
        team_point_counter[key.team_id] = team_point_counter.get(key.team_id, 0) + user_point_counter.get(key)

    return team_point_counter


########################################################################################################################
# Main Function


if __name__ == "__main__":

    db.create_all()

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    application.debug = True

    # make sure templates, etc. are not cached in debug mode
    application.jinja_env.auto_reload = application.debug

    # Use the DebugToolbar
    DebugToolbarExtension(application)

    application.run()
