import os
from datetime import timedelta, datetime, timezone
import bcrypt

from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

from config import config

from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)

jwt = JWTManager(app)
db = SQLAlchemy(app)

from models import UserEncoder, User, TokenBlocklist, find_user_by_username

app.json_encoder = UserEncoder


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username", None)
    if not username or len(username) < app.config["MIN_USERNAME_LENGTH"]:
        return jsonify(
            {'msg': f'The username must be at least {app.config["MIN_USERNAME_LENGTH"]} characters long'}), 422
    # TODO: validate username (only letters and numbers? or ???)
    user = find_user_by_username(username)
    if user:
        return jsonify({"msg": f"Cannot register user: the username '{username}' already exists"}), 409

    email = data.get("email", None)
    if not email:  # TODO: check it's a valid email
        return jsonify({"msg": "Email required"}), 422

    full_name = data.get("full_name", None)
    if not full_name or len(full_name) < app.config["MIN_FULL_NAME_LENGTH"]:
        return jsonify(
            {'msg': f'The full name must be at least {app.config["MIN_FULL_NAME_LENGTH"]} characters long'}), 422

    clear_password = data.get("password", None)
    if not clear_password or len(clear_password) < app.config["MIN_PASSWORD_LENGTH"]:
        return jsonify(
            {'msg': f'The password must be at least {app.config["MIN_PASSWORD_LENGTH"]} characters long'}), 422
    # TODO check other password rules
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(clear_password.encode(), salt)

    user = User(username=username, email=email, full_name=full_name, password=password.decode())
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully", "id": user.id})


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 422

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Wrong username or password"}), 401

    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    access_token = create_access_token(identity=current_user, fresh=False)
    return jsonify(access_token=access_token)


@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def who_am_i():
    return jsonify(current_user)


@app.route("/fresh-only", methods=["GET"])
@jwt_required(fresh=True)
def fresh_only():
    return jsonify(msg="the given token is fresh")


@app.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def modify_token():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
    db.session.commit()
    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")

if __name__ == "__main__":
    app.run(port=6000)
