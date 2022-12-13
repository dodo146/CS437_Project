from flask import Flask, render_template, url_for, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from models.models import *
from flask_bcrypt import Bcrypt
from threading import Thread

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "flask@gmail.com"
app.config['MAIL_PASSWORD'] = "password"
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.refresh_view = 'refresh'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

def send_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'GET':
       return render_template('register.html', form=form) 

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, mail=form.mail.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))


@app.route('/refresh', methods = ["GET", "POST"])
def refresh():
    form = EmailForm()

    if request.method == 'GET':
        return render_template("refresh.html", form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(mail = form.e_mail.data).first()
        if user:
            token = get_reset_token()
            msg = Message()
            msg.subject = "Flask App Password Reset"
            msg.sender = os.getenv('MAIL_USERNAME')
            msg.recipients = [user.mail]
            msg.html = render_template('reset_email.html',
                                user=user, 
                                token=token)
            Thread(target=send_email, args=(app, msg)).start()
        else:
            return f"There is no account with an e-mail: {form.e_mail.data}!",

@app.route('/password_reset_verified/<token>', methods = ['GET','POST'])
def reset_verified(token):
    user = verify_reset_token(token)
    if not user:
        print('no user found')
        return redirect(url_for('login'))
    


if __name__ == "__main__":
    app.run(debug=True)