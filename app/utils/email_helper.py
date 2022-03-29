import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

context = ssl.SSLContext(ssl.PROTOCOL_TLS)

def login_and_send_email(email_config,email_destination,payload):
        message = MIMEMultipart("alternative")
        message["Subject"] = payload["email_subject"]
        message["From"] = "LA Metor API v2"
        message["To"] = email_destination
        message.attach(MIMEText(payload["email_message_txt"], "plain"))
        message.attach(MIMEText(payload["email_message_html"], "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
            server.login(email_config["MAIL_USERNAME"],email_config["MAIL_PASSWORD"])
            server.sendmail(email_config["MAIL_USERNAME"], email_destination, message.as_string())
