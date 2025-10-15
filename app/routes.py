from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import RegistrationForm, LoginForm, CreateGroupForm, AddMemberForm
from app.models import User, GroupMember, FamilyGroup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    groups = []
    if current_user.is_authenticated:
        memberships = current_user.group_memberships
        groups = [membership.group for membership in memberships]
    return render_template("index.html", title='Strona główna', groups=groups)

@app.route("/register", methods=['GET', 'POST'])
def register():
    #przekierowanie zalogowanych użytkowników, aby nie rejestrowali nowego konta
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        #sprawdzenie czy email już istnieje
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Ten adres email jest już zarejestrowany. Spróbuj się zalogować.', 'warning')
            return redirect(url_for('register'))
        
        #dodane na wypadek innych błędów DB
        try:
            hashed_password = generate_password_hash(form.password.data)
            user = User(email=form.email.data, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            flash('Twoje konto zostało pomyślnie utworzone. Możesz się teraz zalogować', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback() #cofnięcie zmian po błędzie
            flash('Wystąpił błąd podczas rejestracji. Spróbuj ponownie.', 'danger')
            # w produkcji logij błąd do pliku
            #logger.error(f"Registration error: {e})

    return render_template("register.html", title="Rejestracja", form=form)

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
    flash('Zostałeś pomyślnie wylogowany', 'success')
    return redirect(url_for('index'))

@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():
        try:
            new_group = FamilyGroup(name=form.name.data)
            new_membership = GroupMember(
                user=current_user,
                group=new_group,
                role='admin')
            db.session.add(new_group)
            db.session.add(new_membership)
            db.session.commit()

            flash(f'Grupa "{new_group.name}" została utworzona.', 'success')
            return redirect(url_for('group_details', group_id=new_group.id))
        except Exception as e:
            db.session.rollback()
            flash('Wystąpił błąd podczas tworzenia grupy. Spróbuj ponownie.', 'danger')

    return render_template('create_group.html', title="Utwórz grupę", form=form)

@app.route('/group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def group_details(group_id):
    form = AddMemberForm()
    group = FamilyGroup.query.get_or_404(group_id)
    
    current_membership = GroupMember.query.filter_by(
        user_id=current_user.id,
        group_id=group.id
    ).first()

    if not current_membership:
        flash('Nie masz dostępu do tej grupy.', 'danger')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        if current_membership.role != 'admin':
            flash('Tylko administrator grupy może dodawać członków.', 'warning')
            return redirect(url_for('group_details', group_id=group_id))
        
        user_to_add = User.query.filter_by(email=form.email.data).first()

        if not user_to_add:
            flash('Użytkownik o tym adresie email nie istnieje.', 'danger')
        elif user_to_add in [m.user for m in group.members]:
            flash('Ten użytkownik jest już członkiem tej grupy.', 'warning')
        else:
            #try-except przy dodawaniu członka
            try:
                new_membership = GroupMember(user=user_to_add, group=group, role='member')
                db.session.add(new_membership)
                db.session.commit()
                flash(f'Użytkownik {user_to_add.email} został dodany do grupy.', 'success')
            except Exception  as e:
                db.session.rollback()
                flash('Wystąpił błąd podczas dodawania członka.', 'danger')
                # W produkcji: app.logger.error(f"Add member error: {e}")

        return redirect(url_for('group_details', group_id=group.id))
    return render_template('group_details.html', title=group.name, group=group, form=form, current_role=current_membership.role)