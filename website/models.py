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
    token = db.Column(db.String(80), nullable=True)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(max=100)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"})

    mail = StringField(validators=[
                             InputRequired(), Length(min=8)], render_kw={"placeholder": "Email"})

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class ChangeForm(FlaskForm):
    mail = StringField(validators=[
                             InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "New Password"})
    submit = SubmitField('Change')


class ForgotForm(FlaskForm):
    mail = StringField(validators=[
                             InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Email"})
    submit = SubmitField('Send Mail')

class ResetForm(FlaskForm):
    mail = StringField(validators=[
                             InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Email"})
    token = StringField(validators=[
                             InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Token"})
    submit = SubmitField('Submit')
