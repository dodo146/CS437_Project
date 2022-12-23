from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


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
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "New Password"})
    submit = SubmitField('Change')


class ForgotForm(FlaskForm):
    mail = StringField(validators=[
                             InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "Email"})
    submit = SubmitField('Send Mail')

class ResetForm(FlaskForm):
    token = StringField(validators=[
                             InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Token"})
    submit = SubmitField('Submit')
