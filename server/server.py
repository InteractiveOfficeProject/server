import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'server.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))