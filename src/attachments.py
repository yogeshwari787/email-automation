"""
src/attachments.py
Generates calendar .ics invites and manages email file attachments (e.g. PDFs, documents).
"""
import os
from pathlib import Path
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta

class AttachmentHandler:
    @staticmethod
    def create_ics_calendar_invite(
        event_title: str,
        start_datetime: datetime,
        duration_minutes: int = 60,
        description: str = "Live training session",
        location: str = "Online / Zoom",
        organizer_email: str = "training@bootcamp.org"
    ) -> str:
        """
        Generates standard RFC 5545 iCalendar (.ics) string.
        Recipients can double-click or accept directly in Gmail / Outlook / Apple Mail.
        """
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        start_str = start_datetime.strftime("%Y%m%dT%H%M%SZ")
        end_str = end_datetime.strftime("%Y%m%dT%H%M%SZ")
        now_str = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        uid = f"{start_str}-{os.urandom(4).hex()}@emailautomation.local"

        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Email Automation System//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{now_str}
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:{event_title}
DESCRIPTION:{description}
LOCATION:{location}
ORGANIZER;CN=Organizer:mailto:{organizer_email}
STATUS:CONFIRMED
BEGIN:VALARM
TRIGGER:-PT15M
ACTION:DISPLAY
DESCRIPTION:Reminder
END:VALARM
END:VEVENT
END:VCALENDAR"""
        return ics_content

    @staticmethod
    def attach_file(message, file_path: Path):
        """Attaches a disk file to a MIMEMultipart message with safe MIME encoding."""
        if not file_path.exists():
            return False

        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{file_path.name}"'
        )
        message.attach(part)
        return True
