from flask import Flask,request,render_template,redirect,url_for,flash,jsonify,session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
import random
from flask_migrate import Migrate
from flask_mail import Mail,Message
import time
from threading import Thread
from flask_login import login_user, login_required, logout_user,UserMixin

def create_database(app):   ### creates database
    if not path.exists('instance/'+ DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database")



db = SQLAlchemy()
DB_NAME = "database.db"


app = Flask(__name__,)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  ## for database 
app.config['SECRET_KEY'] = 'thisisasecretkey'     
app.config['MAIL_SERVER'] = 'smtp.gmail.com' ### for sending mail
app.config['MAIL_PORT'] = '587'              ###
app.config['MAIL_USE_TLS'] = 'True'          ###
app.config['MAIL_USERNAME'] = 'test437odev@gmail.com'  ## created this account for this homework only 
app.config['MAIL_PASSWORD'] = 'yodflknyxpoxxiwy'       ## not the real password but the one google assigns for less secure apps


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
create_database(app)
db.init_app(app)
mail = Mail(app)


class User(db.Model, UserMixin):   # creates database with given columns (username,password etc.)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    mail = db.Column(db.String(40), nullable=False)
    token = db.Column(db.String(80), nullable=True)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



def create_token():                      ###   creates 6 digit token using random library
        _first = random.randint(0,9)     ###   then combines them as a string
        _second = random.randint(0,9)
        _third = random.randint(0,9)
        _fourth = random.randint(0,9)    ### not a sophisticated function but works 
        _fifth = random.randint(0,9)
        _sixth = random.randint(0,9)
        return str(_first)+''+str(_second)+''+str(_third)+''+str(_fourth)+''+str(_fifth)+''+str(_sixth)




def send_mail(user):             ###    creates token using the function above 
    token = create_token()       ###    and then assigns it to the user
    user.token = token           ###    each user has a token field in the database 
    db.session.commit()          ###    which is initialized as null when first registered

    msg = Message(
                'Password Reset Request',
                sender ='test437odev@gmail.com',
                recipients = [user.mail]
               )
               
    msg.body = f'''
        {token}
    '''
    mail.send(msg)
    return 'Sent'



@app.route('/')
def home():
    return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register():

    from models import RegisterForm
    form = RegisterForm()

    if request.method == 'GET':
         return render_template('register.html', form=form)

    if form.is_submitted():
        username = form.username.data
        mail = form.mail.data
        check_username = User.query.filter_by(username = username).first()      ### checks if given name already exists
        check_mail = User.query.filter_by(mail = mail).first()                  ### checks if given mail already exists
        if check_username:
            return jsonify({"message:" : f"There is already a user with username {form.username.data}. Please try again"})
            
        elif check_mail:
             return jsonify({"message:" : f"There is already a user with mail {form.mail.data}. Please try again"})
        else:
            new_user = User(username=form.username.data, password=form.password.data, mail=form.mail.data)
            db.session.add(new_user)   #### adds to the database if given credentials are unique
            db.session.commit()        #### username, mail, password etc. all stored in plain text
            return redirect(url_for('login'))



@app.route("/login", methods = ['GET', 'POST'])
def login():

    from models import LoginForm
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() ## checks database if the given 
        if user:                                                         ## mail actually exists
            if user.password == form.password.data:#   ------>           ## if exists, then checks password
                login_user(user)
                return redirect(url_for('dashboard'))  ## if succesfully logged in, redirects to dashboard
            else:
                flash("Your password is wrong. Please try again")  ## if fails, then redirects to login page 
                return redirect(url_for('login'))
        else:
            return jsonify({"message:" : f"There is no user with a username {form.username.data}. Please try again"})
            ## if can't find user, warns --->> the user does not exist


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/forgot', methods=['GET', 'POST'])
def forgot():

    from models import ForgotForm
    form = ForgotForm()

    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()  ## checks database if the given mail exists 
        if user:
            send_mail(user)  #### sends a mail which includes assigned token
            session["mail"] = user.mail        ### stores the mail in the session 
            return redirect(url_for('token'))  ### in order to use it for future requests  
    return render_template('forgot.html', form=form)



@app.route('/token', methods=['GET', 'POST'])
def token():

    from models import ResetForm
    form = ResetForm()
    user = User.query.filter_by(mail=session["mail"]).first()  ## finds user with the stored session mail

    if form.validate_on_submit():
        if user.token == form.token.data:     ###  compares user's token in database with the token submitted
            return redirect(url_for('change_password'))   ### if matches, redirects to change_password page
    return render_template('reset.html', form=form) #### there is no limit, user can submit tokens infinitely until finds the correct one



@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    
    from models import ChangeForm
    form = ChangeForm()
    user = User.query.filter_by(mail=session["mail"]).first()  ## finds user with the stored session mail

    if form.is_submitted():
        user.password = form.password.data   ### updates user's password 
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('change.html', form=form)
        


if __name__ == "__main__":
    app.run(debug=True)

