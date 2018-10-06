from flask import render_template
from model import db, Point, Team

from os import environ
from jinja2 import StrictUndefined

from flask import Flask


def init_db():
    # set application configuration variables
    application.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # required to use Flask sessions and the debug toolbar
    application.secret_key = environ['FLASK_SECRET_KEY']

    # assign database to Flask applications
    db.app = application
    db.init_app(application)

# Instantiate Flask Application and Database
application = Flask(__name__)
init_db()

# Normally, if you use an undefined variable in Jinja2, it fails silently. Strict undefined raises an error.
application.jinja_env.undefined = StrictUndefined


########################################################################################################################
# Page


@application.route('/')
def index():
    """Homepage."""

    # get points associated with team
    scores = tally_up_team_points_into_dict()
    # get all teams
    teams = Team.query.all()
    # create a list of tuples to hold name and score data to display in rendered template
    teams_scores = [(team.name, scores.get(team.id)) for team in teams]

    return render_template("index.html", teams_scores=teams_scores)


def tally_up_team_points_into_dict():
    """Retrieves points from players and tallies them up into points by team"""

    # set dictionary to hold point values per user and team respectively
    user_point_counter = {}
    team_point_counter = {}

    # retrieve all points
    points = Point.query.all()

    # finds total points for a player and assigns them
    for point in points:
        user_point_counter[point.user] = user_point_counter.get(point.user, 0) + point.points

    # finds total points for a team from players and assigns them
    for key in user_point_counter:
        team_point_counter[key.team_id] = team_point_counter.get(key.team_id, 0) + user_point_counter.get(key)

    return team_point_counter

