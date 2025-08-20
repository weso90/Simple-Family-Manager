from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash(f"Twoje konto zostało pomyślnie utworzone. Możesz się teraz zalogować.")
        return redirect(url_for("index"))

    return render_template("register.html", title="rejestracja", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    #jeśli użytkownik jest zalogowany, przekieruj go na stronę główną
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        #znajdź użytkownika w bazie po email
        user = User.query.filter_by(email=form.email.data).first()

        #sprwadź czy użytkownik istnieje i czy hasło się zgadza
        if user and check_password_hash(user.password, form.password.data):
            #zaloguj użytkownika
            login_user(user, remember=form.remember_me.data)
            flash('Zalogowano pomyślnie!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Logowanie nie powiodło się. Sprawdź email i hasło', 'danger')

    return render_template('login.html', title="Logowanie", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostałeś pomyślnie wylogowany')
    return redirect(url_for('index'))