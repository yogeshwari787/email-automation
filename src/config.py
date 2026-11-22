"""
src/config.py
Loads application configuration and environment variables safely.
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"

# Ensure output directories exist
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class Config:
    DRY_RUN: bool = os.getenv("DRY_RUN", "True").lower() in ("true", "1", "yes")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "True").lower() in ("true", "1", "yes")
    SMTP_USER: str = os.getenv("SMTP_USER", "demo_sender@example.com")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")
    SENDER_NAME: str = os.getenv("SENDER_NAME", "Operations & Automation Desk")
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", SMTP_USER)
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata")
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/email_automation.db")

config = Config()
