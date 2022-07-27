import email
import smtplib, ssl
import datetime
from datetime import date
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def send_m(receiver):
    try:
        print('send_mail.py: Sending email ...')
        password = os.getenv('EMAIL_KEY')
        subject = "Data Atlas"
        body = ("Script run automatically from RPi4 @" + datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S"))
        sender_email = os.getenv('EMAIL')

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver
        message["Subject"] = subject
        message["Bcc"] = receiver  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver, text)
        print('send-mail.py: Email sent successfully !')
    except Exception as e:
        print(e)
        print('send_mail.py: Failed to send email ...')
    
def send_multiple(receiver_emails):
    for receiver in receiver_emails:
        send_m(receiver)
    
# try:
#     receiver_emails = ["jasonraefon@hotmail.com","nino.atlassalesagency@gmail.com"]
#     send_multiple(receiver_emails)

#     # send_m("jasonraefon@hotmail.com")
#     print("Email sent successfully at: ", datetime.datetime.now())
# except Exception as e:
#     print(e)
#     print("Email NOT sent successfully at: ", date.today().strftime("%d %B %Y"))

# send_m('jtsangsolutions@gmail.com')