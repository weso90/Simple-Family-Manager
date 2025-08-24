from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    #relacja łączy się bezpośrednio z modelem pośredniczącym
    #back_populates: ta relacja jest drugą stroną relacji 'user' w klasie GroupMember
    group_memberships = db.relationship('GroupMember', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.email}')"

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#tabela pośrednicząca
class GroupMember(db.Model):
    __tablename__ = 'group_member'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('family_group.id'))
    role = db.Column(db.String(50), nullable=False, default='member')

    user = db.relationship('User', back_populates='group_memberships')
    group = db.relationship('FamilyGroup', back_populates='members')

class FamilyGroup(db.Model):
    __tablename__ = 'family_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    #tabela pośrednicząca do zdefiniowania relacji
    members = db.relationship('GroupMember', back_populates='group', lazy='dynamic')
    
    def __repr__(self):
        return f"FamilyGroup('{self.name}')"