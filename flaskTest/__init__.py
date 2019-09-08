from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b1550409f9179f616eeae71d4710b0be'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'kenanitichi@gmail.com'
app.config["MAIL_PASSWORD"] = 'PurpleX2(1997)'
app.config["MAIL_USE_SSL"] = True
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)

from flaskTest import routes
