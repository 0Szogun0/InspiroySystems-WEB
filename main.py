from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

# Połączenie z bazą danych (lub utworzenie pliku bazy)
conn = sqlite3.connect("moja_baza.db")

# Tworzenie kursora do wykonywania zapytań SQL
cursor = conn.cursor()

# Tworzenie tabeli (jeśli nie istnieje)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        mail TEXT NOT NULL)''')

# Zapisanie zmian i zamknięcie połączenia
conn.commit()
conn.close()

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route("/")
def main():
    return render_template("index.html", title="Strona Główna")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mail = request.form['mail']

        conn = sqlite3.connect('moja_baza.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, mail) VALUES (?, ?, ?)", (username, password, mail))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Użytkownik już istnieje!"
        finally:
            conn.close()

    return render_template("registerform.html", title="Rejestracja do systemu INSPIROY")







@app.route("/loginform")
def loginform():
    return render_template("loginform.html", title="Logowanie do systemu INSPIROY")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get ("password")
        conn = sqlite3.connect('moja_baza.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return render_template("index.html", title="Strona Główna")
        else:
            return "Nieprawidłowe dane logowania!"
    else:
        return render_template("loginform.html", title="Logowanie do systemu INSPIROY")
    
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

    



if __name__ == '__main__':
    app.run(debug=True)