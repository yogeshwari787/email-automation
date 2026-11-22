# System Architecture & Technical Specifications

## 1. Overview
The **Email Automation & Reminder System** is structured in layered tiers:
1. **Data Layer**: CSV flat files (`data/contacts.csv`, `data/reminders.csv`) for student mode, and SQLite/PostgreSQL tables via SQLAlchemy for enterprise mode.
2. **Business & Processing Logic**:
   - `csv_handler.py`: Validates schema, parses boolean opt-outs, and executes inner joins.
   - `renderer.py`: Merges dynamic context dictionaries into Jinja2 / HTML templates.
   - `mailer.py`: SMTP client implementing TLS/SSL security and idempotent mock simulation.
3. **Execution & Scheduling Tier**:
   - `scheduler.py`: Local cron-style scheduler.
   - `run_worker.py`: Async continuous worker evaluating RFC 5545 RRULE recurrence intervals.
4. **Observability & Audit Layer**:
   - `reporter.py`: Produces structured delivery logs and execution metrics.
   - `webhooks.py`: Real-time pixel beacon tracking (`/t/o/{id}.png`) and link tracking (`/t/c/{id}`).

## 2. Idempotency & Delivery Guarantee
To prevent accidental duplicate email dispatches:
- Every planned email generates a unique RFC 2822 `Message-ID`.
- Database message records transition through strict states: `scheduled` → `sent` (or `failed`) → `opened` → `clicked`.
- The worker executes transactions with state locks to ensure a due reminder fires only once per scheduled window.

## 3. Compliance & Anti-Spam (CAN-SPAM / GDPR)
- Every contact record contains an `unsubscribed` boolean.
- The pipeline skips opted-out contacts before template evaluation or SMTP connection.
- Standard unsubscribe headers and footers are appended to all outbound HTML emails.
