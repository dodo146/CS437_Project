from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = 'thisisasecretkey' #for session
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix= "/")
    app.register_blueprint(auth, url_prefix= "/")

    from .models import User
    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database")