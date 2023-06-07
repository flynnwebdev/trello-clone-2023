from flask import Flask
from init import db, ma, jwt, bcrypt
from blueprints.cli_bp import db_commands
from blueprints.cards_bp import cards_bp
from blueprints.users_bp import users_bp
from os import environ

def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(users_bp)
    app.register_blueprint(cards_bp)

    return app
