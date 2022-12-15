from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    mail = db.Column(db.String(40), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(max=100)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"})

    mail = StringField(validators=[
                             InputRequired(), Length(min=8)], render_kw={"placeholder": "Email"})

    submit = SubmitField('Register')


class UserForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(max=20)], render_kw={"placeholder": "Username"})

    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')