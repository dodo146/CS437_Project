from flask import Blueprint,request,render_template,redirect,url_for,flash,jsonify
from .models import LoginForm,RegisterForm,User,ResetForm,ForgotForm,ChangeForm
from flask_login import login_user, login_required, logout_user
from . import db,create_token
from flask_mail import Message


def send_mail(user):
    token = create_token()
    user.token = token
    db.session.commit()

    msg = Message(
                'Hello',
                sender ='test437odev@gmail.com',
                recipients = [user.mail]
               )
               
    msg.body = f'''
        {token}
    '''
    from main import mail
    mail.send(msg)
    return 'Sent'

auth = Blueprint("auth" , __name__)


@auth.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('auth.dashboard'))
            else:
                flash("Your password is wrong. Please try again")
                return redirect(url_for('auth.login'))
        else:
            return jsonify({"message:" : f"There is no user with a username {form.username.data}. Please try again"})

@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
         return render_template('register.html', form=form)

    if form.is_submitted():
        username = form.username.data
        check_username = User.query.filter_by(username = username).first()
        if check_username:
            return jsonify({"message:" : f"There is already a user with username {form.username.data}. Please try again"})
        else:
            new_user = User(username=form.username.data, password=form.password.data, mail=form.mail.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

@auth.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if request.method == 'GET':
         return render_template('forgot.html', form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        if user:
            send_mail(user)
            return redirect(url_for('token'))  ##########
    return render_template('forgot.html', form=form)

        

@auth.route('/token', methods=['GET', 'POST'])
def token():

    form = ResetForm()
    if request.method == 'GET':
         return render_template('reset.html', form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        
        if user:
            if user.token == form.token.data:
                return redirect(url_for('change_password')) ############## change password   BURA DEĞİŞECEK
    return render_template('reset.html', form=form)


@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangeForm()
    if request.method == 'GET':
         return render_template('change.html', form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        user.password = form.password.data
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('change.html', form=form)