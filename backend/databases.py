from flask.cli import with_appcontext
from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy
import click

dbase = SQLAlchemy()

from registration.models import Beneficiaries
from booking.models import Appointment

@click.command("populate")
@click.option("--tables", default="all")
@with_appcontext
def populate_tables(tables):
    click.echo("Initializing registration tables")
    if tables:
        prepopulate()

def initialize_dbase(app):
    dbase.init_app(app)
    dbase.create_all(bind="__all__", app=app)
    app.cli.add_command(populate_tables)

def prepopulate():
    beneficiaries = Beneficiaries("Magido Mascate", 38, "920065440", "msnabmdjaiufakjaonaosf")
    beneficiaries.save()
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


def retrieve_dbase():
    dbase.init_app(current_app)
    yield dbase