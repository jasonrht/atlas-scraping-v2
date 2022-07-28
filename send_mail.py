from email.mime.application import MIMEApplication
from posixpath import basename
import smtplib, ssl
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import pandas as pd
import pandas_to_html

load_dotenv()

def send_m(receiver, filename):
    try:
        print('send_mail.py: Sending email ...')
        password = os.getenv('EMAIL_KEY')
        subject = "Data Atlas"
        sender_email = os.getenv('EMAIL')

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver
        message["Subject"] = subject
        message["Bcc"] = receiver  # Recommended for mass emails

        # Attach files
        with open(f'./PNGs/{filename}', 'rb') as file:
            part = MIMEApplication(file.read(), Name=basename(filename))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
            message.attach(part)

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver, message.as_string())
            server.quit()
        print('send-mail.py: Email sent successfully !')
    except Exception as e:
        print(e)
        print('send_mail.py: Failed to send email ...')
    
def send_multiple(receiver_emails):
    for receiver in receiver_emails:
        send_m(receiver)

def main(png_filename):
    send_m('jtsangsolutions@gmail.com', f'./{png_filename}')

if __name__ == '__main__':
    main()