from flask import Flask, jsonify, render_template, request
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)

app.config.update(dict(
    DATABASE='../database.db',
    DEBUG=True,
    SECRET_KEY='nadim_sarras',
    USERNAME='',
    PASSWORD=''
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/show')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT TITLE FROM pubs WHERE ID = 157803 ORDER BY ID DESC')
    entries = cur.fetchall()
    return render_template('select.html', entries=entries)


@app.route('/', methods=['POST'])
def add_entry():
    db = get_db()
    error = None
    db.execute('INSERT INTO pubs (ID, TITLE, YEAR, JOURNAL, PAGES) VALUES (?, ?, ?, ?, ?)',
               [request.form['ID'], request.form['TITLE'], request.form['YEAR'], request.form['JOURNAL'],
                [request.form['PAGES']]])
    db.commit()
    flash('New entry was successfully posted')
    return render_template(show_entries, error=error)


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    error = None
    if request.method == 'POST':
        flash('Welcome')
        return redirect(url_for('/'))
    return render_template('index.html', error=error)


if __name__ == '__main__':
    app.run()
