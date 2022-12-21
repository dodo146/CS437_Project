from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Message
import random


db = SQLAlchemy()
DB_NAME = "database.db"
login_manager = LoginManager()


def create_token():
        _first = random.randint(0,9)
        _second = random.randint(0,9)
        _third = random.randint(0,9)
        _fourth = random.randint(0,9)
        _fifth = random.randint(0,9)
        _sixth = random.randint(0,9)
        return str(_first)+''+str(_second)+''+str(_third)+''+str(_fourth)+''+str(_fifth)+''+str(_sixth)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = 'thisisasecretkey' #for session
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = '587'
    app.config['MAIL_USE_TLS'] = 'True'
    app.config['MAIL_USERNAME'] = 'test437odev@gmail.com'
    app.config['MAIL_PASSWORD'] = 'cfophsjlgqevppxi'  #'test12345test'
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