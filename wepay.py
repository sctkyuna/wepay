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
	tempEntries = cur.fetchall()
	if not tempEntries:
		error="Event code doesn't exist!"
		return render_template('index.htm', error=error)
	session["eventID"] = eventID
	entries = [[] for j in range(len(tempEntries))]
	
	#TODO: factor this for 	

	for i in range(len(tempEntries)):
		payerUID = tempEntries[i]['payerUID']
		recipUID = tempEntries[i]['recipUID']
		amount = tempEntries[i]['amount']
		payerNameTemp = db.execute("select name from users where ID=?", [payerUID])
		recipNameTemp = db.execute("select name from users where ID=?", [recipUID])
		payerName = payerNameTemp.fetchall()
		recipName = recipNameTemp.fetchall()
		entries[i].append(payerName[0]["firstname"])
		entries[i].append(recipName[0]["firstname"])
		entries[i].append(amount)
	
	event = db.execute("select name from event where ID=?", [eventID])
	eventList = event.fetchall()
	eventName = eventList[0]["name"]
	return render_template('viewevent.htm', eventID=eventID, eventName=eventName, entries=entries)


# if making new event
@app.route('/new', methods=['GET'])
def new_event():
	db = get_db()
	eventID = generateID() # generates random ID that doesn't exist in db
	session["eventID"] = eventID
	db.execute('insert into event values (?, ?, ?)', [eventID, request.args["eventName"], request.args['details']])
	db.commit()
	return render_template('addpeople.htm')


@app.route('/add', methods=['GET', 'POST'])
def add_ppl():
	nameList = request.args.getlist("name")
	phoneList = request.args.getlist("phone")
	db = get_db()
	for i in range(len(nameList)):
		db.execute('insert into users values(NULL, ?, ?)', [nameList[i], phoneList[i]])
	return render_template('viewevent.htm', eventID=session["eventID"])
	# TODO: this should also give eventName and entries



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
