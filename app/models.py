"""
Modele bazy danych dla aplikacji

Struktura:
- User: Użytkownicy aplikacji
- FamilyGroup: Grupy rodzinne
- GroupMember: tabela pośrednicząca User-FamilyGroup z dodatkowym polem 'role'
"""

from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    Model użytkownika.
    UserMixin dodaje metody wymagane przez Flask-Login:
    is_authenticated, is_active, is_anonymous, get_id()
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Hasło zawsze hashowane przez generate_password_hash
    # NIGDY nie przechowujemy plaintext passwords!
    password = db.Column(db.String(128), nullable=False)

    #relacja łączy się bezpośrednio z modelem pośredniczącym
    #back_populates: ta relacja jest drugą stroną relacji 'user' w klasie GroupMember
    group_memberships = db.relationship('GroupMember', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.email}')"

@login.user_loader
def load_user(user_id):
    """
    Callback wymagany przez Flask-Login.
    Ładuje użyutkownika po ID z sesji
    """
    return User.query.get(int(user_id))

class GroupMember(db.Model):
    """
    Tabela pośrednicząca dla relacji Many-to-Many między User i FamilyGroup.

    Używamy explicit association table (zamiast db.Table) bo potrzebujemy:
    - Dodatkowego pola 'role (admin/member)
    - Potencjalnie więcej pól w przyszłości
    """
    __tablename__ = 'group_member'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('family_group.id'))

    # Role: 'admin' (może zarządzać grupą) lub 'member' (tylko pogląd)
    role = db.Column(db.String(50), nullable=False, default='member')

    # Relacje do User i FamilyGroup
    user = db.relationship('User', back_populates='group_memberships')
    group = db.relationship('FamilyGroup', back_populates='members')

class FamilyGroup(db.Model):
    """
    Model grupy rodzinnej
    """
    __tablename__ = 'family_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relacja do członków przez tabelę pośredniczącą
    # lazy='dynamic' pozwala na .filter(), .count() itp.
    members = db.relationship('GroupMember', back_populates='group', lazy='dynamic')
    
    def __repr__(self):
        return f"FamilyGroup('{self.name}')"