import json
import bcrypt
from flask_jwt_extended import get_current_user
from sqlalchemy import func

from app import db


def find_user_by_username(username):
    return User.query.filter_by(username=username).one_or_none()


class UserEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            return {
                "id": o.id,
                "username": o.username,
                "email": o.email,
                "full_name": o.full_name
            }
        else:
            return super().default(o)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text(), nullable=False)
    full_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def check_password(self, password):
        if not password:
            return False
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey('users.id'),
        default=lambda: get_current_user().id,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False,
    )
