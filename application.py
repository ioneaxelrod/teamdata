from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension
from model import db, Point, Team

from os import environ
from jinja2 import StrictUndefined

from flask import Flask

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Required to use Flask sessions and the debug toolbar
application.secret_key = environ['FLASK_SECRET_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails silently. Strict undefined raises an error.
application.jinja_env.undefined = StrictUndefined

########################################################################################################################
# Page


@application.route('/')
def index():
    """Homepage."""

    # scores = tally_up_team_points_into_dict()
    # teams = Team.query.all()
    # teams_scores = [(team.name, scores.get(team.id)) for team in teams]


    point = Point.query.first()
    teams_scores = []

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

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    application.debug = True
    # make sure templates, etc. are not cached in debug mode
    application.jinja_env.auto_reload = application.debug

    # Configure to use our MySQL database
    db.init_app(application)
    application.app_context().push()
  #  db.app = application


    if not db.engine:
        print("no engine")

    db.engine.connect()
    print("connection XYZ FARTBARF")


    # Use the DebugToolbar
    DebugToolbarExtension(application)

    application.run(port=5000, host='0.0.0.0')