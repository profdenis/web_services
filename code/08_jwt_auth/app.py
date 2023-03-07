import bcrypt

from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///users3.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["MIN_USERNAME_LENGTH"] = 4
app.config["MIN_FULL_NAME_LENGTH"] = 3
app.config["MIN_PASSWORD_LENGTH"] = 8

jwt = JWTManager(app)
db = SQLAlchemy(app)

from models import UserEncoder, User, find_user_by_username

app.json_encoder = UserEncoder


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


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

    user = find_user_by_username(username)
    if not user or not user.check_password(password):
        return jsonify({"msg": "Wrong username or password"}), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def who_am_i():
    return jsonify(current_user)


if __name__ == "__main__":
    app.run()
