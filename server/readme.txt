Start the Server:


sqlite3 server/interactive_office.db < server/schema.sql
export FLASK_APP=server/server.py
export FLASK_DEBUG=true
flask run



