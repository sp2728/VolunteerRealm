from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

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


def register_blueprints(app):

    from auth.models import User
    from auth.auth import auth as auth_blueprint
    from core.main import main as main_blueprint

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

def setup_database(app):
    with app.app_context():

        db.create_all()
        _admins = ('SaiKiran@gmail.com', 'va123@gmail.com', 'jinalshah542@gmail.com','voluteeradmin@gmail.com')
        from auth.models import User, Permission
        user = User.query.filter_by(name="System").first()
        if user is None:
            password = 'password'
            user = User(email="voluteeradmin@gmail.com",name="System",password=generate_password_hash(password,method='sha256'),first_name='first_name',last_name='last_name',phone_number='43123',gender='Male',permission=Permission.USER)
            db.session.add(user)
            db.session.commit()

        users = User.query.filter(User.email.in_(_admins)).all()
        for user in users:
            user.permission = Permission.ADMIN

        db.session.commit()

if __name__ == "__main__":
    app = create_app()
    setup_database(app)
    app.run(debug=True)
