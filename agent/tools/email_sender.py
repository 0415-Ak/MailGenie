import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(to_emails, subject: str, body: str):
    """
    Supports single email (string) OR multiple emails (list).
    """

    # Convert to list if single string

    if isinstance(to_emails, str):
        to_emails = [to_emails]

    # Create message

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = ", ".join(to_emails)   

    # Send email
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(
            SMTP_EMAIL,
            to_emails,   
            msg.as_string()
        )

