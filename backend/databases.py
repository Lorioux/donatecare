from flask.cli import with_appcontext
from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy
import click

dbase = SQLAlchemy()

from backend.registration.models import Beneficiaries, Doctors, Specialities, Licenses
from backend.scheduling.models import Schedules

from backend.booking.models import Appointment

@click.command("populate")
@click.option("--tables", default="all")
@with_appcontext
def populate_tables(tables):
    click.echo("Initializing registration tables")
    prepopulate(tables)

@click.command("delete")
@click.option("--tables", default="all")
@with_appcontext
def erase_tables(tables):
    click.echo("Initializing tables: {}".format(tables))
    delete(tables)

def initialize_dbase(app):
    dbase.init_app(app)
    dbase.create_all(bind="__all__", app=app)
    app.cli.add_command(populate_tables)
    app.cli.add_command(erase_tables)

def prepopulate(tables):
    
    all_tables = initialized_tables()

    if tables=="all":
        for tbl in all_tables:
            tbl.save()
    else:
        tbl = all_tables[tables]
        tbl.save()

def delete(tables):
    
    all_tables = initialized_tables()

    if tables=="all":
        for tbl in all_tables:
            dbase.session.delete(tbl)
            dbase.session.commit()
    else:
        tbl = all_tables[tables]
        dbase.session.delete(tbl)
        dbase.session.commit()

def initialized_tables():
    beneficiaries = Beneficiaries("Magido Mascate", 38, "920065440", "msnabmdjaiufakjaonaosf")
    appointments = Appointment(
        date="04/07/2021", 
        time="12:00", 
        doctName="Dr. John Doe", 
        doctSpeciality="Nutricionist", 
        doctIdentity="cacascavavavavavaefvagsfafdaadfavbadgsefaegfvgsbsgfva", 
        beneficiaryName="Magido Mascate", 
        beneficiaryPhone="351920000000", 
        beneficiaryNif = "mmndmajdladandadmasjscavavadcavasavsd"
    )
    
    doctors = Doctors("Dr. John Doe", "351920450000", "acsvavadvfvadv", "saacvadvadvasdfvacavav", "Av. Carolina Michaelis")

    specs = Specialities("Nutricionist", "Nutricionist professional", doctors.id)
    
    scheds = Schedules('date', 'time', 'week', 'year', doctors.id)

    return {
        "beneficiaries": beneficiaries,
        "appointments" : appointments,
        "doctors" : doctors,
        "specialities": specs, 
        "schedules" : scheds,
    }
        

def retrieve_dbase():
    dbase.init_app(current_app)
    yield dbase