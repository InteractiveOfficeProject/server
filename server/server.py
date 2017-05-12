import os
import sqlite3
import json
import queue
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'interactive_office.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

break_queue = queue.Queue
# each element: []


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    rv.row_factory = make_dicts
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application contect.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database"""
    init_db()
    print('Initialized the database')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/")
def hello():
    db = get_db()
    if request.method == "GET":
        username_from_post = request.args.get('username', 'default get')
        sql_command = """INSERT INTO activity(name, maximumUsers) VALUES (?, ?)"""
        values = ('hello', 5)
        cur = db.execute(sql_command, values)
        db.commit()
        print(cur.lastrowid)
        return "GET request with username = %s" % username_from_post
    elif request.method == "POST":
        username_from_post = request.args.get('username', 'default post')
        return "POST request with username = %s" % username_from_post


@app.route("/activities", methods=['GET'])
def get_activities():
    db = get_db()
    cur = db.execute('select activityId, name, maximumUsers from activity order by activityId desc')
    activities = cur.fetchall()
    print(activities)
    return jsonify(activities)


@app.route("/ping", methods=['GET'])
def ping_request():
    db = get_db()
    username = request.args.get('username', 'default get')
    activity_counter = 0
    global break_queue
    if break_queue.has_has(username):
        activity = break_queue.get(username)[0]
        for key, value in break_queue.items():
            if value[0] == activity:
                activity_counter += 1

        # count number of people in queue with same activity & waiting, if >=2 return match found,
        # - remove user from queue
        # elif activity.maximumUsers > 2
        # true -> check if break with same activity in last 3 minutes was matched, join
        # false -> return code 100
        cur = db.execute('select ')
    # else return error code 406


@app.route("/signup", methods=['POST'])
def signup_for_break():
    db = get_db()
    userid = request.args.get('UserID', 'default get')
    activities = request.args.get('ActivityIDs', 'default get')
    sql_command_break = """INSERT INTO break (user, activity, room) VALUES (?,?,?)"""
    value_break = (userid, 0, 0)
    cur = db.execute(sql_command_break, value_break)
    sql_command_activities = """INSERT INTO activitiesForBreak (break, activity) VALUES (?,?,?)"""
    sql_command_breakid_search = """select max(breakId) from break"""
    cur = db.execute(sql_command_breakid_search)
    breakId = cur.fetchall()[0]["breakId"]
    for activity in activities:
        cur = db.execute(sql_command_activities, (breakId, activity))
    db.commit()


if __name__ == '__main__':
    app.run()
