from flask import Blueprint
from werkzeug.security import *

auth = Blueprint("auth", __name__, url_prefix="memberAuth")


@auth.route("/login")
def login():
    pass

@auth.route("/logout")
def logout():
    pass