
import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = "inspiroysystems@gmail.com"
EMAIL_PASSWORD = "yzev apby ugqg pemx"
m = "mwDWADAWDAW"

msg = EmailMessage()
msg['Subject'] = 'Check out Bronx as a puppy!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = '0yaeshogun0@gmail.com'

# Treść HTML z dynamiczną zmienną `m`
html_content = f"""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
        <p>The variable value is: {m}</p>
    </body>
</html>
"""

# Dodanie alternatywnej treści HTML
msg.add_alternative(html_content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)