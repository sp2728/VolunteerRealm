from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .core.main import main as main_blueprint
from .auth.models import User
from .auth.auth import auth as auth_blueprint


def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # db.create_all(app=create_app())
    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    # init SQLAlchemy so we can use it later in our models
    db = SQLAlchemy();
    app.config['SECRET_KEY'] = 'change_me_to_something_else'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)