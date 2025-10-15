"""
Widoki dla aplikacji.

Każda trasa obsługuje:
1. Walidację danych wejściowych
2. Logikę biznesową
3. Operacje w bazie danych
4. Flash messages dla użytkownika
5. Przekierowania
"""

from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import RegistrationForm, LoginForm, CreateGroupForm, AddMemberForm, EditGroupForm
from app.models import User, GroupMember, FamilyGroup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    """
    Strona główna aplikacji.

    Dla zalogowanych: lista grup
    Dla niezalogowanych: landing page
    """
    groups = []
    if current_user.is_authenticated:
        # pobierz wszystkie członkostwa użytkownika
        memberships = current_user.group_memberships
        # Wyciągnij grupy z członkostw
        groups = [membership.group for membership in memberships]
    return render_template("index.html", title='Strona główna', groups=groups)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Rejestracja nowego użytkownika.

    Zabezpieczenia:
    - Sprawdzanie unikalności emaila przez dodaniem do bazy
    - Hashowanie hasła
    - Try-except na wypadek błędów
    """
    # Zalogowani użytkownicy nie powinni widizeć formularza rejestracji
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        #sprawdzenie czy email już istnieje
        #bez tego dostaniemy crash aplikacji
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Ten adres email jest już zarejestrowany. Spróbuj się zalogować.', 'warning')
            return redirect(url_for('register'))
        
        # Try-except chroni przed nieoczekiwanymi błędami
        try:
            #hasło zawsze hashowane - werkzeug.security
            hashed_password = generate_password_hash(form.password.data)
            user = User(email=form.email.data, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            flash('Twoje konto zostało pomyślnie utworzone. Możesz się teraz zalogować', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            # Kluczowy rollback - bez tego sesja zostaje z niechcianymi danymi
            db.session.rollback()
            flash('Wystąpił błąd podczas rejestracji. Spróbuj ponownie.', 'danger')

            # w produkcji logij błąd do pliku
            #logger.error(f"Registration error: {e})

    return render_template("register.html", title="Rejestracja", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Logowanie użytkownika
    """
    # jeśli użytkownik jest zalogowany, przekieruj go na stronę główną
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        # Znajdź użytkownika po email
        user = User.query.filter_by(email=form.email.data).first()

        # Sprawdź czy użytkownik istnieje i czy hasło się zgadza
        # check_password_hash porównuje hash z bazy z wprowadzonym hasłem
        if user and check_password_hash(user.password, form.password.data):
            # Flask-Login zarządza sesją
            # remember=True tworzy "remember me" w cookie
            login_user(user, remember=form.remember_me.data)
            flash('Zalogowano pomyślnie!', 'success')
            return redirect(url_for('index'))
        else:
            # nie ujawniaj czy email czy hasło jest złe (względy bezpieczeństwa)
            flash('Logowanie nie powiodło się. Sprawdź email i hasło', 'danger')

    return render_template('login.html', title="Logowanie", form=form)

@app.route('/logout')
@login_required # tylko zalogowani mogą się wylogować
def logout():
    """
    Wylogowanie użytkownika - czyści sesję
    """
    logout_user()
    flash('Zostałeś pomyślnie wylogowany', 'success')
    return redirect(url_for('index'))

@app.route('/create_group', methods=['GET', 'POST'])
@login_required 
def create_group():
    """
    Tworzenie nowej grupy rodzinnej.
    
    Proces:
    1. Utwórz grupę
    2. Utwórz członkostwo z rolą 'admin'
    3. Dodaj OBA do sesji i commituj razem
    """
    form = CreateGroupForm()
    if form.validate_on_submit():
        try:
            # Nowa grupa
            new_group = FamilyGroup(name=form.name.data)

            # Twórca grupy automatycznie staje się adminem
            new_membership = GroupMember(
                user=current_user,
                group=new_group,
                role='admin')
            
            # Dodaj oba obiekty - SQLAlchemy automatycznie ustawi IDs po commit
            db.session.add(new_group)
            db.session.add(new_membership)
            db.session.commit()

            flash(f'Grupa "{new_group.name}" została utworzona.', 'success')

            # Przekieruj użytkownika do nowo utworzonej grupy
            return redirect(url_for('group_details', group_id=new_group.id))
        except Exception as e:
            db.session.rollback()
            flash('Wystąpił błąd podczas tworzenia grupy. Spróbuj ponownie.', 'danger')
            # w produkcji: app.logger.error(f"Create group error: {e}")

    return render_template('create_group.html', title="Utwórz grupę", form=form)

@app.route('/group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def group_details(group_id):
    """
    Szczegóły grupy + dodawanie członków.

    KLUCZOWE ZABEZPIECZENIE:
    sprawdzamy czy current_user należy do grupy przez pokazaniem danych.
    Bez tego każdy zalogowany mógłby zobaczyć wszyskie grupy
    """
    form = AddMemberForm()

    # get_or_404: zwróć grupę lub 404 jeżeli nie istnieje
    group = FamilyGroup.query.get_or_404(group_id)
    
    # autoryzacja: spraweź czy użytkownik należy do grupy
    current_membership = GroupMember.query.filter_by(
        user_id=current_user.id,
        group_id=group.id
    ).first()

    # jeżeli nie należy do grupy - odmowa dostępu
    if not current_membership:
        flash('Nie masz dostępu do tej grupy.', 'danger')
        return redirect(url_for('index'))

    #obsługa dodawania członków (tylko dla admina)
    if form.validate_on_submit():
        # Sprawdź uprawnienia - tylko admin może dodawać członków
        if current_membership.role != 'admin':
            flash('Tylko administrator grupy może dodawać członków.', 'warning')
            return redirect(url_for('group_details', group_id=group_id))
        
        #znajdź użytkownika do dodania
        user_to_add = User.query.filter_by(email=form.email.data).first()

        #walidacja czy użytkownik istnieje i czy należy do grupy
        if not user_to_add:
            flash('Użytkownik o tym adresie email nie istnieje.', 'danger')
        elif user_to_add in [m.user for m in group.members]:
            flash('Ten użytkownik jest już członkiem tej grupy.', 'warning')
        else:
            # wszystko ok - dodaj członka
            try:
                new_membership = GroupMember(user=user_to_add, group=group, role='member') #nowi członkowie zawsze jako 'member'
                db.session.add(new_membership)
                db.session.commit()
                flash(f'Użytkownik {user_to_add.email} został dodany do grupy.', 'success')
            except Exception  as e:
                db.session.rollback()
                flash('Wystąpił błąd podczas dodawania członka.', 'danger')
                # W produkcji: app.logger.error(f"Add member error: {e}")

        # redirect żeby uniknąć ponownego wysłania formularza przy odświeżeniu
        return redirect(url_for('group_details', group_id=group.id))
    
    # Renderuj szablon z danymi grupy
    return render_template('group_details.html', title=group.name, group=group, form=form, current_role=current_membership.role)

@app.route('/group/<int:group_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    """
    Edycja nazwy grupy (tylko admin)
    """

    form = EditGroupForm()
    group = FamilyGroup.query.get_or_404(group_id)

    #sprawdź czy użytkownik należy do grupy
    current_membership = GroupMember.query.filter_by(
        user_id=current_user.id,
        group_id=group.id
    ).first()

    if not current_membership:
        flash('Nie masz dostępu do tej grupy', 'danger')
        return redirect(url_for('index'))
    
    #tylko admin może edytować
    if current_membership.role != 'admin':
        flash('Tylko administrator może edytować grupę.', 'warning')
        return redirect(url_for('group_details', group_id=group.id))
    
    if form.validate_on_submit():
        try:
            old_name = group.name
            group.name = form.name.data
            db.session.commit()

            flash(f'Nazwa grupy zmieniona z "{old_name}" na "{group.name}".', 'success')
            return redirect(url_for('group_details,', group_id=group.id))
        
        except Exception as e:
            db.session.rollback()
            flash('Wystąpił błąd podczas edycji grupy.', 'danger')

    #wypełnij formularz obecną nazwą
    if not form.is_submitted():
        form.name.data = group.name

    return render_template('edit_group.html', )

@app.route('/group/<int:group_id/remove_member/<int:user_id>', methods=['POST'])
@login_required
def remove_member(group_id, user_id):
    """
    Usuwanie członka z grupy (tylko administrator).

    Nie można usunąć ostatniego admina
    """
    group = FamilyGroup.query.get_or_404(group_id)

    #sprawdź czy current_user jest adminem
    current_membership = GroupMember.query.filter_by(
        user_id=current_user.id,
        group_id=group.id
    ).first()

    if not current_membership or current_membership.role != 'admin':
        flash('Tylko administrator może usuwać członków.', 'warning')
        return redirect(url_for('group_details', group_id=group.id))
    
    #znajdź członkostwo do usunięcia
    membership_to_remove = GroupMember.query.filter_by(
        user_id=user_id,
        grupy_id=group_id
    ).first_or_404()

    # nie pozwól usunąć siebie jeśli jesteś jedynym adminem
    if user_id == current_user.id:
        #sprawdź czy są inni admini
        admin_count = GroupMember.query.filter_by(
            group_id=group_id,
            role='admin'
        ).count()

        if admin_count <= 1:
            flash('Nie możesz usunąć siebie - jesteś jedynym administratorem grupy.', 'warning')
            return redirect(url_for('group_details', group_id=group.id))
        
    try:
        user_email = membership_to_remove.user.email
        db.session.delete(membership_to_remove)
        db.session.commit()

        flash(f'Użytkownik {user_email} został usunięty z grupy', 'success')

    except Exception as e:
        db.session.rollback()
        flash('Wystąpił błąd podczas usuwania członka.', 'danger')

    return redirect(url_for('group_details', group_id=group.id))