import sqlite3
from datetime import datetime
import click
from flask import current_app, g

# get the database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# close the database connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# initialize the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# initialize the database command
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# register the timestamp converter
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

# initialize the app
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)