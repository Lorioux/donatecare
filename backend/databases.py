import sys
sys.path.append("..")

import click
from flask.cli import with_appcontext
from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import Session

dbase = SQLAlchemy()

def initializer(key, kwargs):
    if kwargs.keys().__contains__(key):
        return kwargs[key]
    return None

from backend.booking.models import Appointment
from backend.registration.models import (Beneficiary, Doctor, License, Country,
                                         Speciality, MemberAddress)
from backend.scheduling.models import Schedule


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

    if tables == "all":
        for tbl in all_tables.values():
            tbl.save()
    else:
        click.echo("Working on table. " + tables)
        tbl = all_tables[tables]
        tbl.save()


def delete(tables):
    instantes = {
        "beneficiaries": Beneficiary(),
        "appointments": Appointment(),
        "doctors": Doctor(),
        "specialities": Speciality(),
        "schedules": Schedule(),
    }

    all_tables = initialized_tables()
    with Session(dbase.engine) as session, session.begin():
        if tables == "all":
                try:
                    for tbl in instantes:
                        session.delete(tbl)
                except:
                    session.rollback()
                else:
                    session.commit()    
        else:
            instante = session.query(instantes[tables])
            stmt = delete(instantes[tables]).Where(instantes[tables].doctor_nif == instante.doctor_nif)
            session.delete(stmt)
            session.commit()


def initialized_tables():
    beneficiary = Beneficiary(
        "Magido Mascate", 38, "920065440", "msnabmdjaiufakjaonaosf",
        addresses="mcaosmdasdasdasddasdasnadass"
    )

    appointment = Appointment(
        date="04/07/2021",
        time="12:00",
        doctName="Dr. John Doe",
        doctSpeciality="Nutricionist",
        doctIdentity="cacascavavavavavaefvagsfafdaadfavbadgsefaegfvgsbsgfva",
        beneficiaryName="Magido Mascate",
        beneficiaryPhone="351920000000",
        beneficiaryNif="mmndmajdladandadmasjscavavadcavasavsd",
    )

    doctor = Doctor(
        name="Dr. John Doe",
        phone="351920450000",
        nif="acsvavadvfvadv",
        mode="saacvadvadvasdfvacavav",
        photo="msoadnsandoasdas",
        speciality = "msdamsn,dkaksdalsdamlsda",
        address = "dasmddoaosdmasdkaslmaosnasfa",
        license= "sacmsiandiaidaosdnaosdas"
    )

    speciality = Speciality(title="Nutricionist", details="Nutricionist professional", doctor_id=1)

    schedule = Schedule(date="date", time="time", week="week", year="year", doctor_id=1)

    return {
        "beneficiaries": beneficiary,
        "appointments": appointment,
        "doctors": doctor,
        "specialities": speciality,
        "schedules": schedule,
    }


# def retrieve_dbase():
#     dbase.init_app(current_app)
#     yield dbase
