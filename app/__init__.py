"""
Inicjalizacja aplikacji Flask i konfiguracja rozszerzeń.

Moduł tworzy instancję aplikacji i konfiguruje:
- SQLAlchemy (ORM ddo bazy danych) - możliwość szybkiej zmiany typu bazy danych
- Flask-Migrate - migracje bazy danych
- Flask-Login - autentykacja użytkowników
- zmienne środowiskowe przez python-dotenv
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
# WAŻNE .env w .gitignore - wrażliwe dane
load_dotenv()

app = Flask(__name__)

# Konfiguracja SECRET_KEY ze zmiennych środowiskowych
# w produkcyjnej aplikacji zmienić!
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'klucz-zastepczy-zmienic-w-produkcji'

# Konfiguracja bazy danych - domyślnie SQLite dla prostoty
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'

# Wyłącz tracking modyfikacji - oszczędza pamięć i nie jest używany
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicjalizacja rozszerzeń
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

#g Konfiguracja Flask-Login
login.login_view = 'login' # Gdzie przekierować niezalogowanych użytkowników
login.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'
login.login_message_category = 'info' # Kategoria dla flash message

# Import na końcu żeby uniknąć circular imports (routes i models potrzebują 'app' i 'db')
from app import routes, models