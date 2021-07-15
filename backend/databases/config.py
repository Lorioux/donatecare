from __future__ import absolute_import 

import click
from flask.cli import with_appcontext
from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy, declarative_base
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session
from flask_migrate import Migrate

dbase = SQLAlchemy()


migrate = Migrate()

Base = declarative_base()

def initializer(key, kwargs):
    if kwargs.keys().__contains__(key):
        return kwargs[key]
    return None


@click.command("populate")
@click.option("--tables", default="all")
@with_appcontext
def populate_tables(tables):
    click.echo("Initializing all tables")
    initialize_dbase(current_app)


@click.command("delete")
@click.option("--tables", default="all")
@with_appcontext
def erase_tables(tables):
    click.echo("Deleting all tables: {}".format(tables))
    delete()


def initialize_dbase(app):
    # dbase.init_app(app)
    migrate.init_app(app, dbase)
    dbase.create_all(bind="__all__", app=app)
    app.cli.add_command(populate_tables)
    app.cli.add_command(erase_tables)


def delete():
    dbase.drop_all()
    dbase.session.commit()
