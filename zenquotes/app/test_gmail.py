import smtplib, os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
msg = MIMEText("Hello from MindFuel test via Gmail SMTP.")
msg["Subject"] = "SMTP Test"
msg["From"] = os.getenv("MAIL_USER")
msg["To"] = os.getenv("MAIL_USER")

with smtplib.SMTP(os.getenv("MAIL_HOST"), int(os.getenv("MAIL_PORT"))) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.getenv("MAIL_USER"), os.getenv("MAIL_PASSWORD"))
    server.sendmail(msg["From"], msg["To"], msg.as_string())

print("✅  Test email sent successfully!")
