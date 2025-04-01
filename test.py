from flask import request, redirect, url_for, render_template, Flask
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mail = request.form['mail']

        # Prosta walidacja
        if not username or not password or not mail:
            return "Wszystkie pola są wymagane."

        # Haszowanie hasła

        conn = sqlite3.connect('moja_baza.db')
        cursor = conn.cursor()

        # Sprawdzanie, czy użytkownik już istnieje
        print(f"Sprawdzanie użytkownika: username={username}, mail={mail}")  # Logowanie
        cursor.execute("SELECT * FROM users WHERE username = ? OR mail = ?", (username, mail))
        existing_user = cursor.fetchone()
        print(f"Znaleziony użytkownik: {existing_user}")  # Logowanie

        if existing_user:
            return "Użytkownik lub email już istnieje!"

        try:
            cursor.execute("INSERT INTO users (username, password, mail) VALUES (?, ?, ?)", (username, password, mail))
            conn.commit()
        except Exception as e:
            return f"Problem z rejestracją: {str(e)}"
        finally:
            conn.close()

    return render_template("registerform.html", title="Rejestracja do systemu INSPIROY")

if __name__ == '__main__':
    app.run(debug=True)