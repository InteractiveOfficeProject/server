import os
import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'interactive_office.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

break_queue = {}


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
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
        return "GET request with username = %s" %username_from_post
    elif request.method == "POST":
        username_from_post = request.args.get('username', 'default post')
        return "POST request with username = %s" % username_from_post


@app.route("/activities", methods=['GET'])
def get_activities():
    db = get_db()
    cur = db.execute('select name, maximumUsers from activity order by activityId desc')
    activities = cur.fetchall()
    return jsonify(activities)


@app.route("/ping", methods=['GET'])
def ping_request():
    db = get_db()
    username = request.args.get('username', 'default get')
    global break_queue
    if break_queue.has_has(username):
        # count number of people in queue with same activity, if >=2 return match found, remove user from queue
        # elif activity.maximumUsers > 2
        # true -> check if break with same activity in last 3 minutes was matched, join
        # false -> return code 100
        cur = db.execute('select ')
    # else return error code 406


if __name__ == '__main__':
    app.run()
