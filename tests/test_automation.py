"""
tests/test_automation.py
Unit and integration tests for email personalization, CSV handling, and dry-run dispatch.
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.renderer import EmailRenderer
from src.csv_handler import CSVHandler
from src.mailer import EmailSender
from src.reporter import ExecutionReporter

def test_contacts_csv_loading():
    contacts = CSVHandler.load_contacts()
    assert len(contacts) > 0
    assert "email" in contacts[0]
    assert "name" in contacts[0]

def test_reminders_csv_loading():
    reminders = CSVHandler.load_reminders()
    assert len(reminders) > 0
    assert "reminder_id" in reminders[0]
    assert "contact_id" in reminders[0]

def test_merge_contacts_and_reminders():
    merged = CSVHandler.merge_contacts_and_reminders()
    assert len(merged) > 0
    for record in merged:
        assert "name" in record
        assert "reminder_id" in record

def test_email_renderer():
    renderer = EmailRenderer()
    context = {
        "name": "Test User",
        "company": "Acme Inc",
        "role": "QA Engineer",
        "course_name": "Python Automation",
        "session_time": "18:00 IST",
        "timezone": "UTC"
    }
    subj, html = renderer.render_subject_and_body(
        subject_template="Hello {{ name }}",
        template_filename="reminder_template.html",
        context=context
    )
    assert subj == "Hello Test User"
    assert "Test User" in html
    assert "Python Automation" in html

def test_dry_run_mailer():
    mailer = EmailSender(dry_run=True)
    res = mailer.send_email(
        recipient_name="Tester",
        recipient_email="test@example.com",
        subject="Test Run",
        html_content="<p>Hello</p>"
    )
    assert res["status"] == "simulated_sent"
    assert res["mode"] == "dry_run"
    assert "message_id" in res

def test_reporter_summary():
    sample_records = [
        {"status": "simulated_sent"},
        {"status": "simulated_sent"},
        {"status": "failed"},
        {"status": "skipped"}
    ]
    summary = ExecutionReporter.generate_summary(sample_records)
    assert summary["total_processed"] == 4
    assert summary["sent_or_simulated"] == 2
    assert summary["failed"] == 1
    assert summary["skipped_unsubscribed"] == 1
    assert summary["success_rate_percent"] == 50.0

if __name__ == "__main__":
    test_contacts_csv_loading()
    test_reminders_csv_loading()
    test_merge_contacts_and_reminders()
    test_email_renderer()
    test_dry_run_mailer()
    test_reporter_summary()
    print("ALL TESTS PASSED SUCCESSFULLY (6/6)!")
