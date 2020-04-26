import functools

from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from flask_mail import Mail
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'volunteerrealm@gmail.com',
    "MAIL_PASSWORD": 'volunteerRealm123'
}


def admin_only(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if current_user and current_user.is_authenticated and current_user.is_admin():
            return f(*args, **kwargs)
        else:
            flash("You are not authenticated to this page")
            return redirect(url_for('user.userDashboard'))
    return wrap


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'change_me_to_something_else'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    register_blueprints(app)
    setup_database(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    app.config.update(mail_settings)
    mail.init_app(app)

def register_blueprints(app):

    from auth.models import User
    from auth.auth import auth as auth_blueprint
    from core.main import main as main_blueprint
    from admins.admins import admin as admin_blueprint
    from users.users import user as user_blueprint

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)


def setup_database(app):
    with app.app_context():
        from auth.models import User, Permission

        db.create_all()
        _admins = ["voluteeradmin1223@gmail.com", "varshaahuja13@gmail.com", "saikiran1298@gmail.com", "xyz@gmail.com"]
        print("init db, setting up users/admins")

        user = User.query.filter_by(name="System3").first()
        if user is None:
            print('Creating system user')
            password = 'password'
            user = User(email="voluteeradmin1223@gmail.com", name="System3", password=generate_password_hash(password, method='sha256'), first_name='first_name', last_name='last_name', phone_number='433112354', gender='Male', permission=Permission.USER)
            db.session.add(user)
            db.session.commit()

        users = User.query.filter(User.email.in_(_admins)).all()
        for user in users:
            user.permission = Permission.ADMIN

        db.session.commit()


if __name__ == "__main__":
    app = create_app()
