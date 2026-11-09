"""Database helpers - one PostgreSQL connection per request, closed afterwards."""
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g

from app import app


def get_db():
    """Return this request's connection, opening it the first time it is needed."""
    if 'db' not in g:
        g.db = psycopg2.connect(app.config['DATABASE_URL'])
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query_all(sql, params=None):
    """Run a SELECT and return every row as a dictionary."""
    with get_db().cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def query_one(sql, params=None):
    """Run a SELECT and return the first row as a dictionary (or None)."""
    with get_db().cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchone()
