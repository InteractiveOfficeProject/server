#!/bin/bash
DB_FILE=server/interactive_office.db
if [ ! -f $DB_FILE ]; then
    echo "Database file not found. Will be created."
    sqlite3 server/interactive_office.db < server/schema.sql
fi

FLASK_APP=server/server.py FLASK_DEBUG=true flask run
