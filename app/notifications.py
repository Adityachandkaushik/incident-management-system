import smtplib
from email.message import EmailMessage

from flask import current_app


def send_email(to_email, subject, body):

    smtp_username = current_app.config.get(
        "SMTP_USERNAME",
        ""
    )

    smtp_password = current_app.config.get(
        "SMTP_PASSWORD",
        ""
    )

    if not smtp_username or not smtp_password:
        print("SMTP is not configured. Email not sent.")
        return False

    message = EmailMessage()

    message["From"] = current_app.config.get(
        "MAIL_FROM",
        smtp_username
    )

    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(body)

    try:

        with smtplib.SMTP(
            current_app.config.get(
                "SMTP_SERVER",
                "smtp.gmail.com"
            ),
            current_app.config.get(
                "SMTP_PORT",
                587
            )
        ) as server:

            server.starttls()

            server.login(
                smtp_username,
                smtp_password
            )

            server.send_message(message)

        print(f"Email sent successfully to {to_email}")
        return True

    except Exception as error:

        print(f"Email sending failed: {error}")
        return False