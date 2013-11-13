# all the imports
import sqlite3
import RESTRequest
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import logging
import locale
import os
from flask import send_from_directory

# configuration
DATABASE = './RESTAPIClient.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('RESTAPICLIENT_SETTINGS', silent=True)

language, output_encoding = locale.getdefaultlocale()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def show_requests():
    cur = g.db.execute('select request.id, verb, url, status_code from request, response ' +
                        'where request.id = response.fk_request_id ' +
                        'order by request.id desc')
    requests = [dict(id=row[0], verb=row[1], url=row[2], status_code=row[3]) for row in cur.fetchall()]
    return render_template('show_requests.html', requests=requests)


@app.route('/', methods=['POST'])
def add_request():
    if not session.get('logged_in'):
        abort(401)
    # Get form-data:
    protocol = request.form['protocol']
    url = request.form['url']
    headers = ''
    logging.warning('header: %s', request.form)
    # Create request and get response:
    response = RESTRequest.get_data(protocol, url, headers)
    url = response.url
    body = response.text
    status_code = response.status_code
    cur = g.db.execute('select max(id) from request')
    oldId = cur.fetchone()[0]
    if oldId is None:
        newId = 1
    else:
        newId = oldId + 1
    g.db.execute('insert into request (id, verb, url) values (?, ?, ?)',
                 [newId, request.form['verb'], url])
    g.db.execute('insert into response (fk_request_id, status_code, body) values (?, ?, ?)',
                 [newId, status_code, body])
    g.db.commit()
    flash('New request was successfully submitted')
    return redirect(url_for('show_requests'))


@app.route('/favicon.ico')
def favicon():
    logging.warning("Handler for favicon.ico")
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/png')

@app.route('/<requestId>')
def show_request_details(requestId):
    if requestId is None:
        abort(400)
    logging.warning('RequestId: %s', requestId)
    cur = g.db.execute('select request.id, verb, url, status_code, body from request, response ' +
                        'where request.id = response.fk_request_id ' +
                        'and request.id = :Id', {"Id": requestId})
    row = cur.fetchone()
    request.id = row[0]
    request.verb = row[1]
    request.url = row[2]
    request.status_code = row[3]
    request.body = row[4]
    logging.warning( 'Request: %s, %s, %s, %s, %s', request.id, request.verb.encode(output_encoding), request.url, request.status_code, request.body.encode(output_encoding))
    return render_template('show_request_details.html', request=request)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_requests'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_requests'))


if __name__ == '__main__':
    app.run()
