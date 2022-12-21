from website import create_app,login_manager
from website.models import User
from flask_mail import Mail,Message

app = create_app()

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)