from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension
from model import db, Point, Team

from os import environ
from jinja2 import StrictUndefined

from flask import Flask


def create_app():
    temp = Flask(__name__)
    temp.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    temp.secret_key = environ['FLASK_SECRET_KEY']
    temp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    return temp


application = create_app()



# Normally, if you use an undefined variable in Jinja2, it fails silently. Strict undefined raises an error.
application.jinja_env.undefined = StrictUndefined

########################################################################################################################
# Page


@application.route('/')
def index():
    """Homepage."""
    #
    # scores = tally_up_team_points_into_dict()
    # teams = Team.query.all()
    # teams_scores = [(team.name, scores.get(team.id)) for team in teams]
    print("printing out dict")
    application.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    application.secret_key = environ['FLASK_SECRET_KEY']
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    print(application.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
    print("printing out dict done")


    point = Point.query.first()
    print("point: " + str(point))

    teams_scores = []
    foo = point
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

    application.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Required to use Flask sessions and the debug toolbar
    application.secret_key = environ['FLASK_SECRET_KEY']



   # application.app_context().push()
    db.app = application
    db.init_app(application)


    if not db.engine:
        print("no engine")

    db.engine.connect()
    print("connection XYZ FARTBARF")


    # Use the DebugToolbar
    DebugToolbarExtension(application)

    application.run(port=5000, host='0.0.0.0')