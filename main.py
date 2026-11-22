"""
main.py
CLI entrypoint for Email Automation & Reminder System.
Can run in single execution mode, continuous scheduling mode, or dry-run simulation mode.
"""
import argparse
import sys
from datetime import datetime
from src.config import config
from src.csv_handler import CSVHandler
from src.renderer import EmailRenderer
from src.mailer import EmailSender, logger
from src.reporter import ExecutionReporter
from src.scheduler import LocalScheduler

def execute_automation_batch(dry_run: bool = True):
    """
    Core pipeline:
    1. Read Contacts and Reminders from CSV
    2. Filter unsubscribed / inactive
    3. Load and Personalize Email Templates
    4. Dispatch via Mailer (live SMTP or dry-run simulation)
    5. Log status and generate timestamped CSV Delivery Report
    """
    logger.info("="*70)
    logger.info(f"STARTING EMAIL AUTOMATION BATCH RUN [Mode: {'DRY-RUN SIMULATION' if dry_run else 'LIVE PRODUCTION SEND'}]")
    logger.info("="*70)

    try:
        records = CSVHandler.merge_contacts_and_reminders()
    except Exception as e:
        logger.error(f"Failed to load CSV files: {e}")
        return None, {}

    logger.info(f"Loaded {len(records)} scheduled reminder records from CSV database.")

    renderer = EmailRenderer()
    mailer = EmailSender(dry_run=dry_run)
    reporter = ExecutionReporter()

    audit_records = []

    for item in records:
        contact_id = item.get("contact_id")
        name = item.get("name")
        email = item.get("email")
        reminder_type = item.get("reminder_type", "class_reminder")
        title = item.get("title", "Important Update")
        unsubscribed = item.get("unsubscribed", False)
        active = item.get("active", True)

        # Check opt-out and active status
        if unsubscribed:
            logger.warning(f"SKIPPED | Contact '{name}' <{email}> has unsubscribed.")
            audit_records.append({
                "contact_id": contact_id,
                "name": name,
                "email": email,
                "reminder_type": reminder_type,
                "status": "skipped",
                "details": "User unsubscribed (opt-out compliance)",
                "timestamp": datetime.now().isoformat()
            })
            continue

        if not active:
            logger.info(f"SKIPPED | Reminder {item.get('reminder_id')} is marked inactive.")
            continue

        # Choose template based on reminder type
        template_name = "reminder_template.html"
        if reminder_type == "payment_reminder":
            template_name = "payment_reminder.html"

        subject_template = "{{ title }}"
        try:
            rendered_subject, rendered_html = renderer.render_subject_and_body(
                subject_template=subject_template,
                template_filename=template_name,
                context=item
            )
        except Exception as e:
            logger.error(f"TEMPLATE ERROR for {email}: {e}")
            audit_records.append({
                "contact_id": contact_id,
                "name": name,
                "email": email,
                "reminder_type": reminder_type,
                "status": "failed",
                "details": f"Template rendering error: {e}",
                "timestamp": datetime.now().isoformat()
            })
            continue

        # Send or Simulate
        send_result = mailer.send_email(
            recipient_name=name,
            recipient_email=email,
            subject=rendered_subject,
            html_content=rendered_html
        )

        audit_records.append({
            "contact_id": contact_id,
            "name": name,
            "email": email,
            "reminder_type": reminder_type,
            "subject": rendered_subject,
            "status": send_result["status"],
            "message_id": send_result.get("message_id", ""),
            "mode": send_result.get("mode", ""),
            "details": send_result.get("error") or "Delivered successfully",
            "timestamp": datetime.now().isoformat()
        })

    # Save Delivery CSV Report
    report_file = reporter.save_report(audit_records)
    summary = reporter.generate_summary(audit_records)

    logger.info("="*70)
    logger.info(f"BATCH RUN COMPLETED. Audit Report saved to: {report_file}")
    logger.info(f"Summary Metrics: {summary}")
    logger.info("="*70)
    return report_file, summary

def main():
    parser = argparse.ArgumentParser(description="Email Automation & Reminder System CLI")
    parser.add_argument(
        "--mode",
        choices=["dry-run", "send-now", "schedule"],
        default="dry-run",
        help="Execution mode: dry-run (safe simulation), send-now (live SMTP), schedule (runs daily scheduler)"
    )
    parser.add_argument(
        "--time",
        default="19:00",
        help="Time to trigger daily reminders in HH:MM format (default: 19:00)"
    )

    args = parser.parse_args()

    if args.mode == "dry-run":
        execute_automation_batch(dry_run=True)
    elif args.mode == "send-now":
        execute_automation_batch(dry_run=False)
    elif args.mode == "schedule":
        scheduler = LocalScheduler()
        logger.info(f"Starting schedule service configured for daily execution at {args.time}...")
        scheduler.schedule_daily(args.time, execute_automation_batch, dry_run=config.DRY_RUN)
        scheduler.run_continuous()

if __name__ == "__main__":
    main()
