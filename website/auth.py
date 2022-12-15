from flask import Blueprint,request,render_template,redirect,url_for,flash
from .models import UserForm,LoginForm,RegisterForm,User
from flask_login import login_user, login_required, logout_user
from . import db



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
            return f"There is no user with the username: {form.username.data}",403

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
        new_user = User(username=form.username.data, password=form.password.data, mail=form.mail.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

@auth.route('/refresh', methods = ["GET", "POST"])
def refresh():
    form = UserForm()

    if request.method == 'GET':
        return render_template("refresh.html", form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(mail = form.e_mail.data).first()
        if user:
            # token = get_reset_token()
            # msg = Message()
            # msg.subject = "Flask App Password Reset"
            # msg.sender = os.getenv('MAIL_USERNAME')
            # msg.recipients = [user.mail]
            # msg.html = render_template('reset_email.html',
            #                     user=user, 
            #                     token=token)
            # Thread(target=send_email, args=(app, msg)).start()
            pass
        else:
            return f"There is no account with an e-mail: {form.e_mail.data}!"