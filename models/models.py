from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app import db
import os
from datetime import time
import jwt


def get_reset_token(self, expires=500):
        return jwt.encode({'reset_password': self.username,
                           'exp':    time() + expires},
                           key=os.getenv('SECRET_KEY_FLASK'))

def verify_reset_token(token):
        try:
            username = jwt.decode(token, key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
            print(username)
        except Exception as e:
            print(e)
            return
        return User.query.filter_by(username=username).first()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    mail = db.Column(db.String(40), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    mail = StringField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Email"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class EmailForm(FlaskForm):
    e_mail = StringField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Email"})

    submit = SubmitField('Refresh')


class RefreshForm(FlaskForm):
    new_password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Please enter your new password"})
    re_entered_password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Please enter your new password again"})
    submit = SubmitField('Refresh')