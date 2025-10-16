# Simple Family Manager (v.0.3)

**Simple Family Manager** to aplikacja webowa napisana w Pythonie z użyciem frameworka Flask, stworzona jako projekt portfolio. Celem aplikacji jest ułatwienie organizacji życia rodzinnego poprzez dostarczenie zestawu prostych w obsłudze, współdzielonych narzędzi.

---

## Funkcjonalności

### Wersja 0.1

* **System autentykacji:** Użytkownicy mogą zakładać nowe konta (e-mail i hasło), logować się i wylogowywać. Hasła są bezpiecznie hashowane.
* **Tworzenie grup rodzinnych:** Po zalogowaniu, użytkownik może stworzyć nową grupę rodzinną, stając się jej pierwszym członkiem i administratorem.
* **Zarządzanie członkami:** Administrator grupy może zapraszać do niej innych, już zarejestrowanych w systemie użytkowników, wpisując ich adres e-mail.
* **Podgląd grup:** Użytkownik widzi listę grup, do których należy, a po kliknięciu może zobaczyć listę członków danej grupy.

### Wersja 0.2

* **Edycja nazwy grupy:** tylko administrator może zmienić nazwę grupy, walidacja 5-15 znaków, historia zmian w flash messages
* **Usuwanie członków z grupy** tylko administrator może usuwać członków, ochrona (nie można usunąć ostatniego administratora), potwierdzenie przed usunięciem, role widoczne przy użytkowniku

### Wersja 0.3

* **Lista zadań (TODO):** tworzenie zadań w ramach grupy, przypisywanie zadań do konkretnych członków rodziny lub pozostawienie jako nieprzypisane, oznaczanie zadań jako ukończone, usuwanie zadań (administrator lub twórca zadania), data i godzina utworzenia zadania

---

## Mapa Rozwoju (Roadmap)

Projekt jest aktywnie rozwijany. Planowane funkcjonalności w kolejnych wersjach to:

* **v.0.3x: Udaskonalanie aplikacji**
    * Więcej opcji opisu użytkownika
    * bootstrap
    * możliwość usuwania grupy
    * więcej możliwości w to-do
* **v.0.4: Wspólna lista zakupów**
    * Dynamiczne dodawanie i usuwanie produktów z listy.
    * Oznaczanie produktów jako "kupione".
* **v.0.5: Wspólny kalendarz**
    * Dodawanie wydarzeń widocznych dla całej rodziny.
    * Ustawianie przypomnień.

## Użyte technologie

* **Backend:** Python 3.x, Flask 3.1.1
* **Baza danych:** SQLite (Flask-SQLAlchemy 3.1.1)
* **Migracje:** Flask-Migrate 4.1.0 (Alembic)
* **Formularze:** Flask-WTF 1.2.2, WTForms 3.2.1
* **Autentykacja:** Flask-Login 0.6.3
* **Hashowanie haseł:** Werkzeug 3.1.3
* **Zmienne środowiskowe:** python-dotenv
* **Frontend:** HTML5, Jinja2, podstawowy CSS

---

## Instalacja i Uruchomienie

*(Sekcja do uzupełnienia w przyszłości)*