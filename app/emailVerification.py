import pyotp
# from .models import User, verification_otps
# import time
from .EmailSender import send_registration_email

secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)

def send_otp(user, email):
    subject = "TimeHackers Email Verification"
    current_otp = str(totp.now())
    message = f"""
    <html>
    <body>
    <p> Greerings, {user}!</p>
    <p> Thanks for choosing Time Hackers! </p>
    <p> Your email verification OTP is: <strong>{current_otp}</strong></p>
    <p> Please, don't share it with anyone else! </p>
    </body>
    </html>
    """
    
    send_registration_email(recipient_email=email, subject=subject, message=message, username=user)
    return current_otp
    