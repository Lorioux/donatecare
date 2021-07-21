from __future__ import absolute_import

from enum import Enum
import uuid
from datetime import (timedelta, datetime)
from functools import wraps
from logging import Logger

import jwt
from sqlalchemy.sql.elements import and_
from flask import Blueprint, request, jsonify, json, session, make_response, current_app
from werkzeug.security import *

from backend.authentication.models import Subscriber, AuthenticationKey


auth = Blueprint("auth", __name__, url_prefix="/Authentication")


class KeyType(Enum):
    TYPE_ONE = (1, "USER_NAME")
    TYPE_TWO = (2, "PUBLIC_ID")
    TYPE_THREE = (3, "PASSWD")


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):

        auth_token = None

        if "x-access-tokens" in request.headers:
            auth_token = request.headers.get("x-access-tokens")

        if auth_token is None:
            return jsonify({"error": "Not authenticated! Try to login again"})

        try:
            data = jwt.decode(auth_token, current_app.config["SECRET_KEY"])
            current_user = Subscriber.query.filter(
                and_(
                    Subscriber.user_name.like(data["user_name"]),
                    Subscriber.password.like(
                        generate_password_hash(data["password"], method="sha256")
                    ),
                )
            ).first()
        except RuntimeError as error:
            Logger("AUTH").error(error)
            return jsonify({"message": "token is invalid"})

        except jwt.ExpiredSignatureError as error:
            Logger("AUTH").error(error)
            return jsonify({"error": "Signature expired. Please log in again."})
        except jwt.InvalidTokenError as error:
            Logger("AUTH").error(error)
            return jsonify({"error": 'Invalid token. Please log in again.'})

        return func(current_user, *args, **kwargs)

    return decorator


@auth.route("/logout")
def logout():
    pass


@auth.route("/createCredentials", methods=["POST"])
def create():
    data = json.loads(request.data)
    passwd = generate_password_hash(data["password"], method="sha256")
    username = data["username"]
    public_id = data["public_id"]
    role = data["role"]
    user = Subscriber(
        user_name=username, password=passwd, public_id=public_id, role=role
    ).save()
    if user is not None:
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
                "iat": datetime.utcnow(),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        response = make_response("Signedup successfully", 200)
        response.set_cookie("token", token)
        return response
    return make_response("Failed to register", 401)


@auth.route("/login", methods=["POST"])
def login():
    authentic = request.authorization

    if not authentic or not authentic.username or not authentic.password:
        return make_response("Could not verify", 401, {"Error": "Login is required"})

    user = Subscriber().query(user_name=authentic.username).first()

    if check_password_hash(user.password, authentic.password):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
                "iat": datetime.utcnow(),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        response = make_response()
        response.set_cookie("token", token.decode("utf-8"))
        return response
        # return jsonify({'token': token.decode('utf-8')})

    return make_response("Could not verify", 401, {"Error": "Login is required"})


@auth.route("/retrievePublicKeys", methods=["POST"])
def create_uuid_value():
    data = json.load(request.data)
    keytype = data["keytype"]
    if keytype in KeyType.TYPE_ONE.value:
        # username
        username = uuid.uuid5(uuid.NAMESPACE_URL, data["value"])
        session["user_id"] = username
        return jsonify({"user_id": username})

    if keytype in KeyType.TYPE_TWO.value:
        public_id = str(uuid.uuid5(uuid.NAMESPACE_URL, data["public_id"]))
        response = make_response({"public_id":public_id}, 200)
        response.set_cookie("public_id", public_id)
        return response
    return make_response()


@auth.route("/addAuthenticationKeys", methods=["POST"])
def add_authentication_keys():

    data = json.loads(request.args.get("data", type=str))
    # response = None
    print(data)
    if "private_key" in data:
        added, object = AuthenticationKey(
                    private_key=data["private_key"], \
                        public_key=data["public_key"]).save()
        if added:
            return jsonify({"id":object.id})