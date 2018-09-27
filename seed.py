from model import *
from os import environ


def create_teams():
    teams = []
    with open("team_seed.txt") as file:
    for line in file:
        data = line.rstrip().split(',')
        name, date_created, date_updated = data
        team = Team(name=name, date_created=date_created, date_updated=date_updated)
        teams.append(team)

    db.session.add_all(teams)
    db.session.commit()


def create_users():
    users = []
    with open("user_seed.txt") as file:
        for line in file:
            data = line.rstrip().split(',')
            name, team_id, date_created, date_updated = data
            user = User(name=name, team_id=team_id, date_created=date_created, date_updated=date_updated)
            users.append(user)

    db.session.add_all(users)
    db.session.commit()


def create_points():
    points = []
    with open("user_seed.txt") as file:
        for line in file:
            data = line.rstrip().split(',')
            user_id, points, reason, date_created = data
            point = Point(user_id=user_id, points=points, reason=reason, date_created=date_created)
            points.append(point)

    db.session.add_all(points)
    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app

    connect_to_db(app)
    db.drop_all()
    db.create_all()

    print("Connected to DB.")
    print("\n\n\n=============================================")

    teams = Team.query.all()
    [print(team) for team in teams]

    print("\n\n\n=============================================")

    users = User.query.all()
    [print(user) for user in users]

    print("\n\n\n=============================================")

    points = Point.query.all()
    [print(point) for point in points]

    print("\n\n\n=============================================")