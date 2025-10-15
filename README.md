# Simple Family Manager (v.0.2)

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

---

## Mapa Rozwoju (Roadmap)

Projekt jest aktywnie rozwijany. Planowane funkcjonalności w kolejnych wersjach to:

* **v.0.3: Wspólna lista zadań (To-Do List)** - W TRAKCIE
    * Tworzenie zadań w ramach grupy.
    * Przypisywanie zadań do konkretnych członków rodziny.
    * Oznaczanie zadań jako ukończone.
* **v.0.4: Wspólna lista zakupów**
    * Dynamiczne dodawanie i usuwanie produktów z listy.
    * Oznaczanie produktów jako "kupione".
* **v.0.5: Wspólny kalendarz**
    * Dodawanie wydarzeń widocznych dla całej rodziny.
    * Ustawianie przypomnień.

## Użyte technologie

* **Backend:** Python, Flask
* **Baza danych:** SQLite (za pośrednictwem Flask-SQLAlchemy)
* **Migracje bazy danych:** Flask-Migrate (Alembic)
* **Formularze:** Flask-WTF
* **Autentykacja:** Flask-Login
* **Frontend:** Prosty HTML z szablonami Jinja2

---

## Instalacja i Uruchomienie

*(Sekcja do uzupełnienia w przyszłości)*