import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "incident-management-secret-key"
    )

    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "database" / "incidents.db")
    )

    SMTP_SERVER = os.getenv(
        "SMTP_SERVER",
        "smtp.gmail.com"
    )

    SMTP_PORT = int(
        os.getenv("SMTP_PORT", "587")
    )

    SMTP_USERNAME = os.getenv(
        "SMTP_USERNAME",
        ""
    )

    SMTP_PASSWORD = os.getenv(
        "SMTP_PASSWORD",
        ""
    )

    MAIL_FROM = os.getenv(
        "MAIL_FROM",
        SMTP_USERNAME
    )