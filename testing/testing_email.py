import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

msg = MIMEText("Test email from agent")
msg["Subject"] = "SMTP Test"
msg["From"] = os.getenv("SMTP_EMAIL")
msg["To"] = os.getenv("SMTP_EMAIL")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(
        os.getenv("SMTP_EMAIL"),
        os.getenv("SMTP_PASSWORD")
    )
    server.send_message(msg)

print("Email sent!")
