from flask import Flask, render_template, request, url_for, session
from note_manager import create_note, get_note
import os
from dotenv import load_dotenv
import smtplib
import ssl

load_dotenv()
app = Flask(__name__)

# Load all secret keys from the .env file
app.secret_key = os.getenv("SECRET_KEY")
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(recipient_email, secret_link):
    subject = "You have received a secret note!"
    body = f"You have been sent a secure, one-time-use note.\nClick the link below to view it. This link will be destroyed after it is read.\n\n{secret_link}"
    message = f"Subject: {subject}\n\n{body}"
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, message)
        return True
    except Exception as e:
        print(f"!!! SERVER ERROR: Failed to send email. Error: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'is_recipient' in session:
        return render_template('access_denied.html')
    if request.method == 'POST':
        secret_content = request.form['message']
        recipient_email = request.form['email']
        note_id = create_note(secret_content)
        secret_link = url_for('view_note', note_id=note_id, _external=True)
        if send_email(recipient_email, secret_link):
            return render_template('link.html', success_message=f"Success! Your secret link has been sent to {recipient_email}.")
        else:
            return "Error: Could not send email. Please check server logs.", 500
    return render_template('index.html')

@app.route('/note/<note_id>')
def view_note(note_id):
    secret_content = get_note(note_id)
    if secret_content:
        session['is_recipient'] = True
        return render_template('note.html', secret_content=secret_content)
    else:
        return render_template('not_found.html')

if __name__ == '__main__':
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("!!! FATAL ERROR: Email credentials not found in .env file.")
    elif not app.secret_key:
        print("!!! FATAL ERROR: SECRET_KEY not found in .env file.")
    else:
        app.run(debug=True)