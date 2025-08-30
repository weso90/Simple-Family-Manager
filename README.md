# Simple Family Manager (v.0.1)

**Simple Family Manager** to aplikacja webowa napisana w Pythonie z użyciem frameworka Flask, stworzona jako projekt portfolio. Celem aplikacji jest ułatwienie organizacji życia rodzinnego poprzez dostarczenie zestawu prostych w obsłudze, współdzielonych narzędzi.

---

## ✨ Funkcjonalności (Wersja 0.1)

Aktualna wersja aplikacji stanowi fundament pod dalszy rozwój i oferuje podstawowe funkcje zarządzania użytkownikami i grupami:

* **System autentykacji:** Użytkownicy mogą zakładać nowe konta (e-mail i hasło), logować się i wylogowywać. Hasła są bezpiecznie hashowane.
* **Tworzenie grup rodzinnych:** Po zalogowaniu, użytkownik może stworzyć nową grupę rodzinną, stając się jej pierwszym członkiem i administratorem.
* **Zarządzanie członkami:** Administrator grupy może zapraszać do niej innych, już zarejestrowanych w systemie użytkowników, wpisując ich adres e-mail.
* **Podgląd grup:** Użytkownik widzi listę grup, do których należy, a po kliknięciu może zobaczyć listę członków danej grupy.

---

## 🛠️ Użyte technologie

* **Backend:** Python, Flask
* **Baza danych:** SQLite (za pośrednictwem Flask-SQLAlchemy)
* **Migracje bazy danych:** Flask-Migrate (Alembic)
* **Formularze:** Flask-WTF
* **Autentykacja:** Flask-Login
* **Frontend:** Prosty HTML z szablonami Jinja2

---

## ⚙️ Instalacja i Uruchomienie

*(Sekcja do uzupełnienia w przyszłości)*

---

## 🚀 Mapa Rozwoju (Roadmap)

Projekt jest aktywnie rozwijany. Planowane funkcjonalności w kolejnych wersjach to:

* **v.0.2: Rozbudowa profili i grup**
    * Możliwość edycji nazwy grupy.
    * Usuwanie członków z grupy przez administratora.
    * Rozbudowane profile użytkowników (np. awatar, imię).
* **v.0.3: Wspólna lista zadań (To-Do List)**
    * Tworzenie zadań w ramach grupy.
    * Przypisywanie zadań do konkretnych członków rodziny.
    * Oznaczanie zadań jako ukończone.
* **v.0.4: Wspólna lista zakupów**
    * Dynamiczne dodawanie i usuwanie produktów z listy.
    * Oznaczanie produktów jako "kupione".
* **v.0.5: Wspólny kalendarz**
    * Dodawanie wydarzeń widocznych dla całej rodziny.
    * Ustawianie przypomnień.