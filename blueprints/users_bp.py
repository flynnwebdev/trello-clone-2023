from flask import Blueprint, request
from datetime import timedelta
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.user import User, UserSchema

users_bp = Blueprint("users", __name__)


@users_bp.route("/register", methods=["POST"])
def register():
    try:
        # Parse, sanitize and validate the incoming JSON data
        # via the schema
        user_info = UserSchema().load(request.json)
        # Create a new User model instance with the schema data
        user = User(
            email=user_info["email"],
            password=bcrypt.generate_password_hash(user_info["password"]).decode(
                "utf-8"
            ),
            name=user_info["name"],
        )

        # Add and commit the new user
        db.session.add(user)
        db.session.commit()

        # Return the new user, excluding the password
        return UserSchema(exclude=["password"]).dump(user), 201
    except IntegrityError:
        return {"error": "Email address already in use"}, 409


@users_bp.route("/login", methods=["POST"])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json["email"])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json["password"]):
            token = create_access_token(
                identity=user.email, expires_delta=timedelta(days=1)
            )
            return {"token": token, "user": UserSchema(exclude=["password"]).dump(user)}
        else:
            return {"error": "Invalid email address or password"}, 401
    except KeyError:
        return {"error": "Email and password are required"}, 400
