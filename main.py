from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import smtplib
from email.message import EmailMessage
import uuid


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
cursor.execute('''CREATE TABLE IF NOT EXISTS vv (
                        username TEXT NOT NULL,
                        token TEXT NOT NULL)''')

# Zapisanie zmian i zamknięcie połączenia
conn.commit()
conn.close()

app = Flask(__name__)
app.secret_key = 'supersecretkey'

EMAIL_ADDRESS = "inspiroysystems@gmail.com"
EMAIL_PASSWORD = "kaij ccsn fbql kkij"
def sendemail():
    msg = EmailMessage()
    msg['Subject'] = 'WERYFIKACJA KONTA'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = '0yaeshogun0@gmail.com'
    # Treść HTML z dynamiczną zmienną `m`
    html_content = f"""\
        <!DOCTYPE html>
        <html>
        <body>
            <h1 style="color:Blue;">Dziękujemy za rejestrację :D</h1>
            <h2 style="color:Blue;">Kliknij poniżej by się zweryfikować:</h2>
            <p>
                <a href="https://www.example.com" style="background-color: #4CAF50; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; border-radius: 8px;">Zweryfikuj konto</a>
            </p>
            
        </body>
    </html>
    """


    msg.add_alternative(html_content, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


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
            cursor.execute("INSERT INTO users (username, password, mail, vv) VALUES (?, ?, ?, ?)", (username, password, mail, "0"))
            token = str(uuid.uuid4())
            cursor.execute("INSERT INTO vv (username, token) VALUES (?, ?)", (username, token))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Użytkownik już istnieje!"
        finally:
            conn.close()

    return render_template("registerform.html", title="Rejestracja do systemu INSPIROY")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get ("password")
        conn = sqlite3.connect('moja_baza.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.execute("SELECT vv FROM users WHERE username = ?", (username,))
        vv = cursor.fetchone()
        conn.close()

        if user:
            if vv and vv[0] == "1":
                session['username'] = username
                return render_template("index.html", title="Strona Główna")
            else:
                return render_template("notvv.html")
        else:
            return "Nieprawidłowe dane logowania!"
    else:
        return render_template("loginform.html", title="Logowanie do systemu INSPIROY")
    

@app.route("/login/vv/<token>")
def ver(token):
    conn = sqlite3.connect('moja_baza.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM vv WHERE token = ?", (token,))
    vv2 = cursor.fetchone()
    if vv2:
        cursor.execute('''UPDATE users SET vv = ? WHERE username = ?''', ("1", vv2[0]))
        cursor.execute('''DELETE FROM vv WHERE token = ?''', (token,))
        conn.commit()
    else:
        return "Błąd"
    conn.close()
    return "Zweryfikowano"
    
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

    



if __name__ == '__main__':
    app.run(debug=True)