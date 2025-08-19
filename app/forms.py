from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło',
                             validators=[DataRequired()])
    password2 = PasswordField('Powtórz Hasło',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

