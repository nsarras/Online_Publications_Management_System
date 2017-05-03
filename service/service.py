from flask import Flask, jsonify, g, request
from sqlite3 import dbapi2 as sqlite3

DATABASE = '../database.db'
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def add_author(name, iden):
    sql = "INSERT INTO authors (AUTHOR, auth_ID) VALUES('%s','%d')" % (name, int(iden))
    print sql
    db = get_db()
    db.execute(sql)
    res = db.commit()
    return res


def find_author(name=''):
    sql = "SELECT TITLE from pubs, authors WHERE AUTHOR = %s" % "\"" + name + "\""
    print sql
    db = get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    rv.close()
    return res[0]


@app.route('/')
def users():
    return jsonify(hello='Nadim Sarras')


@app.route('/add', methods=['POST'])
def add_user():
    print (add_author(name=request.form['name'], iden=request.form['iden']))
    return ''


@app.route('/find_auth')
def find_author_by_name():
    author_info = request.args.get('name', '')
    give_back = find_author(author_info)
    print give_back
    return jsonify(TITLE=give_back['title'])


if __name__ == '__main__': app.run(debug=True)
