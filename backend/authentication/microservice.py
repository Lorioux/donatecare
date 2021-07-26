from __future__ import absolute_import

from enum import Enum
import uuid
from datetime import (timedelta, datetime)
from functools import wraps
from logging import Logger
import base64

import jwt
from sqlalchemy.sql.elements import and_
from flask import Blueprint, request, jsonify, json, session, make_response, current_app
from werkzeug.security import *

from backend.authentication.models import Subscriber,  AuthenticationKey


auth = Blueprint("auth", __name__, url_prefix="/authentication")


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
            return jsonify({"error": "Not dataated! Try to login again"})

        try:
            data = jwt.decode(auth_token, current_app.config["SECRET_KEY"], algorithms="HS256")
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
def create_credencials():
    data = json.loads(request.data)
    
    passwd = generate_password_hash(data["password"], method="sha256")
    username = data["phone"]
    fullname = generate_password_hash(data["fullname"], method="sha256")
    public_id = uuid.uuid3(uuid.NAMESPACE_URL, "{}-{}".format(data["phone"],data["role"]))
    data["password"] = passwd
    data["username"] = username 
    data["fullname"] = fullname
    data["publicid"] = str(public_id)

    subscriber = Subscriber(data=data)
    exists, user = subscriber.validate()
    if exists:
        return make_response({"response":"Failed to register with provided data."}, 401)
    
    user = subscriber.save()
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
        response = make_response({'response':"Subscribed successfully"}, 200)
        response.set_cookie("token", token)
        response.headers.set("access_token", token)
        return response
    


@auth.route("/login", methods=["POST"])
def login():
    data = json.loads(request.data)

    if not data or not data["userid"] or not data["password"] or not data["role"]:
        print(1)
        return make_response({"Error":"Could not verify", "message": "Either role, or whatsapp id or password is missing!"}, 401, )

    user = Subscriber(data={}).get_one(data["userid"], data["role"])

    if user is None:
        print(2)
        print(user)
        return make_response({"Error":"Could not verify", "message": "Subscribe to get started!"}, 401, )

    if check_password_hash(user.password, data["password"]):
        print(3)
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
                "iat": datetime.utcnow(),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        response = make_response({"response": "Logged in successfully"})
        response.set_cookie("token", token)
        response.headers.add_header("access_token", f"Bearer {token}")
        return response


@auth.route("/retrievePublicKeys", methods=["POST"])
def create_uuid_value():
    data = json.loads(request.data)
    keytype = data["keytype"]
    print(data)
    if keytype in KeyType.TYPE_ONE.value:
        # username
        username = uuid.uuid5(uuid.NAMESPACE_URL, data["value"])
        session["user_id"] = username
        return jsonify({"user_id": username})

    if keytype in KeyType.TYPE_TWO.value:
        public_id = str(uuid.uuid5(uuid.NAMESPACE_URL, data["value"]))
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
        added, object =  AuthenticationKey(
                    private_key=data["private_key"], \
                        public_key=data["public_key"]).save()
        if added:
            return jsonify({"id":object.id})


        