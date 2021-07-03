import click
from flask.cli import with_appcontext
from flask import current_app

from flask_sqlalchemy import SQLAlchemy, declarative_base


dbase = SQLAlchemy()
Base = declarative_base()

from models import Appointment


@click.command("populate")
@click.option("--tables", default="all")
@with_appcontext
def populate_tables(tables):
    click.echo("Initializing booking tables")
    if tables:
        prepopulate() 

def initialize_database(app):
    app.cli.add_command(populate_tables)
    dbase.init_app(app)
    dbase.create_all(bind="__all__", app=app)
    

def prepopulate():
    appointment = Appointment(
        date="04/07/2021", 
        time="12:00", 
        doctName="Dr. John Doe", 
        doctSpeciality="Nutricionist", 
        doctIdentity="cacascavavavavavaefvagsfafdaadfavbadgsefaegfvgsbsgfva", 
        beneficiaryName="Magido Mascate", 
        beneficiaryPhone="351920000000", 
        beneficiaryNif = "mmndmajdladandadmasjscavavadcavasavsd"
    )
    appointment.save()

def retrieve_database():
    with current_app.app_context():
        dbase.init_app(current_app)
        yield dbase