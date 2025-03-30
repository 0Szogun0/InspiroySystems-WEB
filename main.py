from flask import Flask, render_template, redirect, url_for, request
import sqlite3

# Połączenie z bazą danych (lub utworzenie pliku bazy)
conn = sqlite3.connect("moja_baza.db")

# Tworzenie kursora do wykonywania zapytań SQL
cursor = conn.cursor()

# Tworzenie tabeli (jeśli nie istnieje)
cursor.execute('''
CREATE TABLE IF NOT EXISTS uzytkownicy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imie TEXT,
    wiek INTEGER
)
''')

# Zapisanie zmian i zamknięcie połączenia
conn.commit()
conn.close()

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html", title="Strona Główna")

@app.route("/loginform")
def loginform():
    return render_template("loginform.html", title="Logowanie do systemy INSPIROY")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get ("password")
        print(username)
        print(password)
        print("to był test XDD")
        return redirect(url_for('loginform'))

    



if __name__ == '__main__':
    app.run(debug=True)