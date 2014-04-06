import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import string
import random
import pdb
def generateID(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'wepay.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('WEPAY_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# if event already exists
@app.route('/view', methods=['POST', 'GET'])
def view_event():
	db = get_db()
	eventID = request.args['eventID']
	cur = db.execute("select payerUID, recipUID, amount from trans where eventID=?", [eventID])
	entries = cur.fetchall()
	event = db.execute("select name from event where ID=?", [eventID])
	eventName = event.fetchall()
	
	return render_template('viewevent.htm', eventName=eventName, entries=entries)


# if making new event
@app.route('/add', methods=['GET'])
def make_find_event():
	db = get_db()
	eventID = generateID() # generates random ID that doesn't exist in db
	db.execute('insert into event values (?, ?, ?)', [eventID, request.args["eventName"], request.args['details']])
	db.commit()
	return render_template('addpeople.htm', eventID=eventID)

@app.route('/db')   
def dbtest():
    db = connect_db()
    cursor = db.cursor()
    init_db()
        
@app.route('/')
def main():
	return render_template('index.htm') 
    
if __name__ == '__main__':
    app.run(debug=True)
