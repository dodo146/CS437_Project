from website import create_app,login_manager,db,create_token
from website.models import User
from flask_mail import Mail,Message
from flask_migrate import Migrate

app = create_app()

mail = Mail(app)
migrate = Migrate(app, db)

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
    mail.send(msg)
    return 'Sent'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)