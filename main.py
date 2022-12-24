from flask import Flask,request,render_template,redirect,url_for,flash,jsonify,make_response
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
import random
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail,Message
import time
from threading import Thread
from flask_login import login_user, login_required, logout_user,UserMixin

def create_database(app):
    if not path.exists('instance/'+ DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database")

def create_token():
        _first = random.randint(0,9)
        _second = random.randint(0,9)
        _third = random.randint(0,9)
        _fourth = random.randint(0,9)
        _fifth = random.randint(0,9)
        _sixth = random.randint(0,9)
        return str(_first)+''+str(_second)+''+str(_third)+''+str(_fourth)+''+str(_fifth)+''+str(_sixth)


def check_time(user):
   while True:
    time.sleep(300)
    from main import app
    with app.app_context():
        from models import User
        all_user = User.query.all()
        for c_user in all_user:
                if c_user == user:
                    if c_user.token != None:
                        c_user.token = None
                        db.session.commit()


def send_mail(user):
    token = create_token()
    user.token = token
    db.session.commit()
    x = Thread(target=check_time,daemon=True,args=[user])
    x.start()

    msg = Message(
                'Hello',
                sender ='test437odev@gmail.com',
                recipients = [user.mail]
               )
               
    msg.body = f'''
        {token}
    '''
    mail.send(msg)
    return 'Sent'

db = SQLAlchemy()
DB_NAME = "database.db"


app = Flask(__name__,)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SECRET_KEY'] = 'thisisasecretkey' #for session
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = 'True'
app.config['MAIL_USERNAME'] = 'test437odev@gmail.com'
app.config['MAIL_PASSWORD'] = 'cfophsjlgqevppxi'  #'test12345test'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
create_database(app)
db.init_app(app)
limiter = Limiter(app, key_func=get_remote_address)
mail = Mail(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    mail = db.Column(db.String(40), nullable=False)
    token = db.Column(db.String(80), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))



@app.route('/')
def home():
    return render_template('home.html')


@app.route("/login", methods = ['GET', 'POST'])
def login():
    from models import LoginForm
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Your password is wrong. Please try again")
                return redirect(url_for('login'))
        else:
            return jsonify({"message:" : f"There is no user with a username {form.username.data}. Please try again"})



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    from models import RegisterForm
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
            return redirect(url_for('login'))

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    from models import ForgotForm
    form = ForgotForm()
    if request.method == 'GET':
         return render_template('forgot.html', form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        if user:
            send_mail(user)
            res = make_response(redirect(url_for('token')))
            res.set_cookie('_mail', user.mail, max_age=None)
            return res 
    return render_template('forgot.html', form=form)


@app.route('/token', methods=['GET', 'POST'])
@limiter.limit('5 per day')
def token():
    
        from models import ResetForm
        form = ResetForm()
        if request.method == 'GET':
            return render_template('reset.html', form=form)
        if form.validate_on_submit():
            user = User.query.filter_by(mail=request.cookies.get('_mail')).first()
            if user.token == form.token.data:
                res = make_response("Cookie Removed")
                res.set_cookie('_mail', user.mail, max_age=0)
                res = make_response(redirect(url_for('change_password')))
                res.set_cookie('_mail', user.mail, max_age=None)
                return res
        return render_template('reset.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
   
        from models import ChangeForm
        form = ChangeForm()
        if request.method == 'GET':
            return render_template('change.html', form=form)
        if form.is_submitted():
            user = User.query.filter_by(mail=request.cookies.get('_mail')).first()
            res = make_response("Cookie Removed")
            res.set_cookie('_mail', user.mail, max_age=0)
            user.password = form.password.data
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('change.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)

