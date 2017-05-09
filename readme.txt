Start the Server:


sqlite3 server/interactive_office.db < server/schema.sql
export FLASK_APP=server/server.py
export FLASK_DEBUG=true
flask run


The application will then listen to port 5000. The available routes are
documented at http://pivanics.users.cs.helsinki.fi/interactive-office-api-documentation
