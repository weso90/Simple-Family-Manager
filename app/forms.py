from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło',
                             validators=[DataRequired()])
    password2 = PasswordField('Powtórz Hasło',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło',
                             validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class CreateGroupForm(FlaskForm):
    name = StringField('Nazwa Grupy', validators=[DataRequired()])
    submit = SubmitField('Stwórz Grupę')

class AddMemberForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Dodaj członka')