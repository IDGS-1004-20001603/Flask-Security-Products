from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from .models.Models import User, Role, db
from flask_wtf.csrf import CSRFProtect
import os

userDataStore = SQLAlchemySessionUserDatastore(db.session, User, Role)
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/flasksecurity'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    csrf.init_app(app)

    db.init_app(app)

    @app.before_first_request
    def create_all():
        db.create_all()

    security = Security(app, userDataStore)

    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
