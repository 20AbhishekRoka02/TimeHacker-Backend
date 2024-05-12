# from json import load
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()

def send_registration_email(recipient_email,  subject, message, username=None):
    # Your Gmail credentials
    sender_email = os.environ['EMAIL_ID']
    sender_password = os.environ['APP_PASSWORD']
    # print(sender_password)

    # Create the email message
    subject = subject
    message = message
    # f"""
    # <html>
    # <body>
    # <p>Greetings, {username}!</p>

    # <p>Congratulations on your successful registration with our MoU Generator. Following is your College ID:
    # <strong>{user_id}</strong></p>

    # <p>Please, don't share it with anyone else!</p>
    # </body>
    # </html>
    # """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__=="__main__":
    # Example usage
    username = "JohnDoe"
    user_id = "12345"
    recipient_email = "rockst463@gmail.com"
    send_registration_email(username, user_id, recipient_email)
