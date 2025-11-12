import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
from datetime import datetime


# Email configuration
MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


# Send email function
def send_email(to_email, quote, author, name, frequency="daily"):
    first_name = name.split()[0] if name else "there"
    try:
        # Message container
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your {frequency} Dose of Wellness ✨"
        msg["From"] = "no-reply@mindfuel.com"
        msg["To"] = to_email

        # Plain-text mail version
        text_body = f"""
            Hi {first_name},

            Here’s your dose of calm and clarity for today:

            “{quote}”
            — {author}

            Take a moment to breathe, stretch, or simply sit with this thought.
            Small reminders like these help you realign with what matters most—your peace, your growth, your balance.

            See you tomorrow for another spark of inspiration 🌿

            Warmly,
            The MindFuel Team
        """

        # HTML mail version
        html_body = f"""
        <html>
          <body style="font-family: Georgia, sans-serif; line-height: 1.6; color: #333;">
            <p>Hi <b>{first_name}</b>,</p>

            <p>Here's your dose of calm and clarity today:</p>

            <blockquote style="font-style: italic; color: #333;">
              “{quote}”<br>
              — <b>{author}</b>
            </blockquote>
            
            <p style="margin-top: 25px;">Warmly,<br>
            <b>The MindFuel Team</b><br>
            <a href="https://www.mindfuel.app" style="color:#388e3c; text-decoration:none;">www.mindfuel.app</a></p>
          </body>
        </html>
        """

        # Attach both versions
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        # Send via SMTP
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(MAIL_USER, MAIL_PASSWORD)
            server.sendmail(msg["From"], msg["To"], msg.as_string())

        # Logging
        logging.info(f"Email sent successfully to {to_email}")
        return True
    
    except smtplib.SMTPException as e:
        logging.error(f"Failed to send email to {to_email}: {e}")
        return False


# Send daily summary report to admin
def send_summary_email(summary, admin_email="iamomowale@outlook.com"):
    sent = summary.get("sent", 0)
    failed = summary.get("failed", 0)

    subject = f"MindFuel Daily Summary — {os.getenv('ENV_NAME', 'Production')}"
    body = (
        f"Daily Email Summary — {datetime.now().date()}\n"
        f"{'-'*40}\n"
        f"Sent:   {sent}\n"
        f"Failed: {failed}\n\n"
        "Check logs/app.log for more info.\n\n"
        "Stay inspired,\n"
        "MindFuel Bot"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "no-reply@mindfuel.com"
    msg["To"] = admin_email

    try:
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(MAIL_USER, MAIL_PASSWORD)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
        
        logging.info(f"Summary email sent to admin ({admin_email})")
    
    except smtplib.SMTPException as e:
        logging.error(f"Failed to send summary email: {e}")
