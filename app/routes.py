from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import RegistrationForm
from app.models import User
from werkzeug.security import generate_password_hash

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