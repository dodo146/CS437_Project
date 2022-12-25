from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


class RegisterForm(FlaskForm):
    username = StringField("Username" , validators=[
                           InputRequired(), Length(max=100)], 
                           render_kw={"placeholder": "Username",
                                    "class" : "form-control"})

    password = PasswordField("Password" ,validators=[
                             InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"
                             ,"class" : "form-control"})

    mail = StringField("E-mail",validators=[
                             InputRequired(), Length(min=8)], render_kw={"placeholder": "Email","class" : "form-control"})

    submit = SubmitField('Register',render_kw={"class":"btn btn-pill text-white btn-block btn-primary"})



class LoginForm(FlaskForm):
    username = StringField("Username" , validators=[
                           InputRequired(), Length(max=100)], 
                           render_kw={"placeholder": "Username",
                                    "class" : "form-control"})


    password = PasswordField("Password" ,validators=[
                             InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"
                             ,"class" : "form-control"})

    submit = SubmitField('Login',render_kw={"class":"btn btn-pill text-white btn-block btn-primary"})


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
