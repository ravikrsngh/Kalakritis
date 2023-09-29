from django.core.mail import EmailMultiAlternatives
import random

def send_OTP_email(email):
    otp = random.randint(1000,9999)
    subject, from_email, to = "Welcome to Kalakritis", "ravikrsngh.rks@gmail.com", email
    text_content = f'The otp for registration is {otp}. Thank you.'
    html_content = f"<p>The OTP for registerring with Kalakritis is</p><h2>{otp}</h2><br><br><p>Thank you,<br>Team Kalakritis.</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("Email Sent")
    return otp
