"""
src/mailer.py
Sends emails via standard Python smtplib with TLS or simulated dry-run mode.
"""
import smtplib
import ssl
import email.utils
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any
from .config import config, LOGS_DIR

logger = logging.getLogger("EmailAutomation")
log_file = LOGS_DIR / "email_automation.log"
if not logger.handlers:
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

class EmailSender:
    def __init__(self, dry_run: bool = config.DRY_RUN):
        self.dry_run = dry_run
        self.host = config.SMTP_HOST
        self.port = config.SMTP_PORT
        self.use_tls = config.SMTP_USE_TLS
        self.username = config.SMTP_USER
        self.password = config.SMTP_PASS
        self.sender_name = config.SENDER_NAME
        self.sender_email = config.SENDER_EMAIL

    def send_email(
        self,
        recipient_name: str,
        recipient_email: str,
        subject: str,
        html_content: str,
        text_content: str = None
    ) -> Dict[str, Any]:
        """
        Sends an email or simulates sending in dry-run mode.
        """
        if not recipient_email or "@" not in recipient_email:
            error_msg = f"Invalid recipient email address: '{recipient_email}'"
            logger.error(f"FAILURE | {recipient_name} | {recipient_email} | {error_msg}")
            return {"status": "failed", "error": error_msg, "mode": "validation"}

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = email.utils.formataddr((self.sender_name, self.sender_email))
        message["To"] = email.utils.formataddr((recipient_name, recipient_email))
        message["Date"] = email.utils.formatdate(localtime=True)
        message_id = email.utils.make_msgid()
        message["Message-ID"] = message_id

        if text_content:
            part1 = MIMEText(text_content, "plain", "utf-8")
            message.attach(part1)
        else:
            part1 = MIMEText("Please enable HTML view to read this reminder.", "plain", "utf-8")
            message.attach(part1)

        part2 = MIMEText(html_content, "html", "utf-8")
        message.attach(part2)

        if self.dry_run:
            logger.info(
                f"[DRY-RUN SIMULATION] Email to '{recipient_name}' <{recipient_email}> | Subject: '{subject}' | MessageID: {message_id}"
            )
            return {
                "status": "simulated_sent",
                "message_id": message_id,
                "mode": "dry_run",
                "error": None
            }

        try:
            logger.info(f"Connecting to SMTP server {self.host}:{self.port}...")
            if self.port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
                    server.login(self.username, self.password)
                    server.send_message(message)
            else:
                with smtplib.SMTP(self.host, self.port, timeout=15) as server:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.username, self.password)
                    server.send_message(message)

            logger.info(f"SUCCESS | Sent to {recipient_name} <{recipient_email}> | MessageID: {message_id}")
            return {
                "status": "sent",
                "message_id": message_id,
                "mode": "live_smtp",
                "error": None
            }
        except Exception as e:
            err = f"SMTP Transmission error: {e}"
            logger.error(f"FAILURE | {recipient_email} | {err}")
            return {"status": "failed", "error": err, "mode": "live_smtp"}
