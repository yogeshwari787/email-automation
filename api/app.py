"""
api/app.py
FastAPI application exposing REST endpoints for managing contacts, templates, campaigns, reminders,
and inspecting delivery statistics.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import uuid
from datetime import datetime, timezone

from src.config import config
from src.models import init_db
from src.schemas import ContactCreate, TemplateCreate, CampaignCreate, ReminderCreate
from src.webhooks import router as tracking_router

app = FastAPI(
    title="Email Automation & Reminder API",
    description="Industry-grade email scheduling, tracking, and campaign dispatch system.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tracking_router)
engine = init_db(config.DATABASE_URL)

@app.get("/")
def health_check():
    return {
        "service": "Email Automation & Reminder System",
        "status": "online",
        "dry_run_mode": config.DRY_RUN,
        "timezone": config.TIMEZONE
    }

@app.post("/contacts", status_code=status.HTTP_201_CREATED)
def create_contact(c: ContactCreate):
    with engine.begin() as db:
        cid = str(uuid.uuid4())
        db.execute(
            text("""
                INSERT INTO contacts(id, name, email, company, role, timezone, unsubscribed, created_at)
                VALUES(:i, :n, :e, :c, :r, :tz, 0, :ts)
            """),
            {
                "i": cid, "n": c.name, "e": c.email, "c": c.company or "",
                "r": c.role or "", "tz": c.timezone, "ts": datetime.now(timezone.utc)
            }
        )
        return {"id": cid, "name": c.name, "email": c.email, "status": "created"}

@app.get("/contacts")
def list_contacts():
    with engine.begin() as db:
        res = db.execute(text("SELECT id, name, email, company, role, timezone, unsubscribed FROM contacts")).mappings().all()
        return list(res)

@app.post("/templates", status_code=status.HTTP_201_CREATED)
def create_template(t: TemplateCreate):
    with engine.begin() as db:
        tid = str(uuid.uuid4())
        db.execute(
            text("""
                INSERT INTO templates(id, name, subject, body_md, created_at)
                VALUES(:i, :n, :s, :b, :ts)
            """),
            {"i": tid, "n": t.name, "s": t.subject, "b": t.body_md, "ts": datetime.now(timezone.utc)}
        )
        return {"id": tid, "name": t.name, "status": "created"}

@app.get("/templates")
def list_templates():
    with engine.begin() as db:
        res = db.execute(text("SELECT id, name, subject, body_md, created_at FROM templates")).mappings().all()
        return list(res)

@app.post("/campaigns", status_code=status.HTTP_201_CREATED)
def create_campaign(c: CampaignCreate):
    with engine.begin() as db:
        cid = str(uuid.uuid4())
        db.execute(
            text("""
                INSERT INTO campaigns(id, name, template_id, sender_name, sender_email, created_at)
                VALUES(:i, :n, :t, :sn, :se, :ts)
            """),
            {
                "i": cid, "n": c.name, "t": c.template_id,
                "sn": c.sender_name, "se": c.sender_email, "ts": datetime.now(timezone.utc)
            }
        )
        return {"id": cid, "name": c.name, "status": "created"}

@app.post("/reminders", status_code=status.HTTP_201_CREATED)
def create_reminder(r: ReminderCreate):
    with engine.begin() as db:
        rid = str(uuid.uuid4())
        db.execute(
            text("""
                INSERT INTO reminders(id, title, contact_id, campaign_id, start_at_utc, rrule, active)
                VALUES(:i, :t, :ct, :ca, :st, :rr, 1)
            """),
            {
                "i": rid, "t": r.title, "ct": r.contact_id, "ca": r.campaign_id,
                "st": r.start_at_utc, "rr": r.rrule
            }
        )
        return {"id": rid, "title": r.title, "status": "scheduled"}

@app.get("/messages")
def list_messages():
    with engine.begin() as db:
        res = db.execute(
            text("""
                SELECT m.id, m.campaign_id, m.contact_id, m.scheduled_at_utc, m.sent_at_utc,
                       m.status, m.subject, m.error
                FROM messages m ORDER BY m.scheduled_at_utc DESC LIMIT 50
            """)
        ).mappings().all()
        return list(res)

@app.get("/metrics")
def get_metrics():
    with engine.begin() as db:
        total = db.execute(text("SELECT COUNT(*) FROM messages")).scalar() or 0
        sent = db.execute(text("SELECT COUNT(*) FROM messages WHERE status='sent'")).scalar() or 0
        failed = db.execute(text("SELECT COUNT(*) FROM messages WHERE status='failed'")).scalar() or 0
        opened = db.execute(text("SELECT COUNT(*) FROM messages WHERE status='opened'")).scalar() or 0
        clicked = db.execute(text("SELECT COUNT(*) FROM messages WHERE status='clicked'")).scalar() or 0
        return {
            "total_messages": total,
            "sent": sent,
            "failed": failed,
            "opened": opened,
            "clicked": clicked
        }
