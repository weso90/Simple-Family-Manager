"""
Formularze WTForms dla aplikacji.

Flask-WTF automatycznie dodaje CSRF protection do wszystkich formularzy.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import re

class RegistrationForm(FlaskForm):
    """
    Formularz rejestracji nowego użytkownika.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    #minimalna długość 8 znaków + dodatkowe walidacje w validate_password()
    password = PasswordField('Hasło',
                             validators=[
                                 DataRequired(),
                                 Length(min=8, message='Hasło musi mieć co najmniej 8 znaków.')
                             ])
    password2 = PasswordField('Powtórz Hasło',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_password(self, password):
        """
        Sprawdza czy hasło jest wystarczająco mocne:
        - co najmniej jedna duża litera
        - co najmniej jedna mała litera
        - co najmniej jedna cyfra
        """

        if not re.search(r'[A-Z]', password.data):
            raise ValidationError('Hasło musi zawierać co najmniej jedną dużą literę')
        if not re.search(r'[a-z]', password.data):
            raise ValidationError('Hasło musi zawierać co najmniej jedną małą literę')
        if not re.search(r'\d', password.data):
            raise ValidationError('Hasło musi zawierać co najmniej jedną cyfrę')

class LoginForm(FlaskForm):
    """
    Formularz logowania.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło',
                             validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class CreateGroupForm(FlaskForm):
    """
    Formularz tworzenia nowej grupy rodzinnej.
    """

    # 5-15 znaków - można zmienić w przyszłości
    name = StringField('Nazwa Grupy',
                       validators=[
                           DataRequired(),
                           Length(min=5, max=15, message='Nazwa grupy musi mieć od 5 do 15 znaków')
                       ])
    submit = SubmitField('Stwórz Grupę')

class AddMemberForm(FlaskForm):
    """
    Formularz dodawania członka do grupy (tylko dla adminów).
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Dodaj członka')

class EditGroupForm(FlaskForm):
    """
    Formularz edycji nazwy grupy (tylko dla adminów)
    """

    name = StringField('Nowa nazwa grupy',
                        validators=[
                            DataRequired(),
                            Length(min=5, max=15, message='Nazwa grupy musi mieć od 5 do 15 znaków')
                        ])
    
    submit = SubmitField('Zapisz zmiany')