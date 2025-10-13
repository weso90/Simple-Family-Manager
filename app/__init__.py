from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'klucz-zastepczy-zmienic-w-produkcji'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #oszczędność pamięci - wyłączony tracking modyfikacji

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

#gdzie przekierować niezalogowanych użytkowników
login.login_view = 'login'

#komunikat po przekierowaniu
login.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'
login.login_message_category = 'info'

from app import routes, models