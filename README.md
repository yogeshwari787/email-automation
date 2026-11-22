# 📧 Email Automation & Reminder System

[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Production--Ready](https://img.shields.io/badge/Status-Production--Ready-brightgreen)](#)
[![Zero-Dependency Fallback](https://img.shields.io/badge/Zero--Dependency-Supported-orange)](#)

> An industry-oriented, production-grade Python automation engine that schedules, personalizes, and dispatches automated emails (one-off or recurring), enforces opt-out compliance, tracks opens/clicks, and exports audit delivery reports.

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Problem Statement & Industry Relevance](#-problem-statement--industry-relevance)
3. [Key Features](#-key-features)
4. [System Architecture](#-system-architecture)
5. [Tech Stack Options](#-tech-stack-options)
6. [Folder Structure](#-folder-structure)
7. [Installation & Setup](#-installation--setup)
8. [Configuration & Safe Credentials](#-configuration--safe-credentials)
9. [How to Run (Dry-Run vs Live)](#-how-to-run-dry-run-vs-live)
10. [Virtual Simulation Guide](#-virtual-simulation-guide)
11. [Sample Output & Delivery Reports](#-sample-output--delivery-reports)
12. [Interview Preparation Guide](#-interview-preparation-guide)

---

## 📖 Project Overview
The **Email Automation & Reminder System** automates high-volume, time-sensitive communications including:
- **Training & Live Class Reminders** (e.g., Zoom/Google Meet alerts 30 minutes before class)
- **Payment & Invoice Reminders** (e.g., polite notices for overdue accounts)
- **Webinar & Event Alerts** (e.g., login credentials, calendar triggers)
- **HR & Employee Syncs** (e.g., feedback loops, quarterly review check-ins)

It is designed with **dual-mode flexibility**:
1. **Student / Local CLI Mode**: Runs directly with Python and CSV files, featuring a safe **Virtual Dry-Run Simulation** that mimics SMTP dispatch with zero external dependencies and zero risk of spamming.
2. **Enterprise API & Worker Mode**: Full REST API built with **FastAPI**, **SQLAlchemy**, background worker loop with **RFC 5545 RRULE** recurrence, open/click tracking pixels, and interactive dashboards.

---

## 💼 Problem Statement & Industry Relevance

### The Problem
In modern business operations, manual follow-ups are inefficient, prone to human error, and cause:
- **High No-Show Rates**: Students and attendees forget webinars and classes.
- **Delayed Receivables**: Overdue invoices pile up without scheduled alerts.
- **Lost Staff Productivity**: Teams spend hours manually drafting and sending emails.

### How Companies Use It
- **EdTech & Bootcamps**: Automate daily Zoom links, assignment deadlines, and attendance reminders.
- **Fintech & Accounting**: Dispatch invoices 7 days before, on due date, and 3 days post due date.
- **HR Operations**: Send onboarding drip checklists to incoming hires.
- **Sales & Customer Success**: Re-engage trial leads with structured nudges.

---

## ✨ Key Features
- **Dynamic Personalization**: Auto-injects recipient names, company, amounts, due dates, and courses.
- **Built-in Safe Dry-Run Simulation**: Run complete runs locally without sending real emails or burning SMTP quota.
- **Unsubscribe & Opt-Out Compliance**: Respects user preferences by automatically skipping contacts flagged as unsubscribed.
- **Automated Delivery Audit Reports**: Exports timestamped CSV reports detailing delivery status, message IDs, and errors.
- **Recurrence Engine**: Supports one-off events and recurring alerts (daily/weekly).
- **Zero-Dependency Fallback**: Automatically switches between Pandas/Jinja2 and standard library `csv`/regex if third-party packages are not yet installed.

---

## 🏗️ System Architecture

```text
+-----------------------+     +-----------------------+     +-----------------------+
|   Contacts (CSV/DB)   |     |    Reminders (CSV)    |     |   HTML/Jinja Template |
+-----------------------+     +-----------------------+     +-----------------------+
            │                             │                             │
            └───────────────────────┬─────┴─────────────────────────────┘
                                    ▼
                         [ CSV / Data Handler ]
                     (Validates & Merges on ID)
                                    │
                                    ▼
                         [ Personalization Engine ]
                   (Injects context into HTML & Subject)
                                    │
                                    ▼
                         [ Compliance Filter ]
                 (Checks unsubscribed & active flags)
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
        [ Dry-Run Simulator ]               [ Live SMTP Dispatcher ]
      (Generates Message-ID & Log)        (TLS / SSL over port 587/465)
                  │                                   │
                  └─────────────────┬─────────────────┘
                                    ▼
                         [ Execution Reporter ]
              (Writes timestamped CSV audit report & logs)
                                    │
                                    ▼
          +----------------------------------------------------+
          | Outputs: delivery_report_*.csv & logs/execution.log |
          +----------------------------------------------------+
```

---

## 📁 Folder Structure

```text
Email-Automation-Reminder-System/
│
├── data/                      # Data storage
│   ├── contacts.csv           # Recipient list, timezones, amounts, opt-out status
│   └── reminders.csv          # Reminder schedules, types, titles, recurrence
│
├── templates/                 # Email templates
│   ├── reminder_template.html # Responsive HTML session reminder template
│   ├── payment_reminder.html  # Responsive HTML billing notification template
│   └── reminder_template.txt  # Plain-text fallback template
│
├── src/                       # Core application modules
│   ├── __init__.py
│   ├── config.py              # Environment variable parser
│   ├── csv_handler.py         # CSV loader, validator, and relational joiner
│   ├── renderer.py            # Personalization engine (Jinja2 / built-in fallback)
│   ├── mailer.py              # SMTP sender + Dry-run simulation engine
│   ├── scheduler.py           # Schedule coordinator
│   ├── reporter.py            # Audit report generator and metric calculator
│   ├── models.py              # SQLAlchemy DB models (API mode)
│   ├── schemas.py             # Pydantic schemas (API mode)
│   └── webhooks.py            # Open pixel & click tracking endpoints
│
├── outputs/                   # Generated delivery audit reports (CSV)
│   └── delivery_report_*.csv
│
├── logs/                      # Audit trails and execution logs
│   ├── email_automation.log
│   └── sample_execution.log   # Committed proof-of-work log
│
├── api/                       # REST API (Option B & C)
│   └── app.py                 # FastAPI backend endpoints
│
├── apps/web/                  # Next.js Dashboard (Option C)
│   ├── package.json
│   └── app/page.tsx
│
├── tests/                     # Unit and integration test suite
│   └── test_automation.py
│
├── main.py                    # Primary CLI runner (dry-run, live, schedule)
├── run_worker.py              # Background worker for continuous DB queue
├── streamlit_app.py           # Interactive Streamlit dashboard
├── requirements.txt           # Python library dependencies
├── .env.example               # Safe environment variable template
├── .gitignore                 # Prevents secrets and DB files from leaking
└── README.md                  # Complete documentation
```

---

## ⚡ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/Email-Automation-Reminder-System.git
cd Email-Automation-Reminder-System
```

### 2. Set Up Virtual Environment
```bash
# macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt / PowerShell):
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: If you run without installing dependencies, the system still executes via built-in Python standard library!)*

---

## 🔐 Configuration & Safe Credentials

1. Copy the sample environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and set your preferences:
   ```ini
   # Set to True for safe local testing (zero emails dispatched to external servers)
   DRY_RUN=True

   # SMTP Configuration (Gmail example)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USE_TLS=True

   # Sender credentials
   # For Gmail, generate a 16-character App Password at https://myaccount.google.com/apppasswords
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_16_char_app_password
   SENDER_NAME=Acme Automation Desk
   SENDER_EMAIL=your_email@gmail.com
   ```
> [!CAUTION]
> **Never commit your `.env` file to GitHub.** The `.gitignore` file is pre-configured to keep your credentials strictly local.

---

## 🚀 How to Run

### Mode 1: Dry-Run Simulation (Recommended for Students)
Executes the entire pipeline, personalizes emails, tests compliance, logs actions, and generates a CSV delivery report—**all without sending real emails**:
```bash
python3 main.py --mode dry-run
```

### Mode 2: Live SMTP Send (Real Outbound Emails)
Dispatches genuine emails using the credentials defined in `.env`:
```bash
python3 main.py --mode send-now
```

### Mode 3: Local Daily Scheduler
Runs continuously in the background and fires batches at a specified time:
```bash
python3 main.py --mode schedule --time 19:00
```

### Mode 4: Run Tests
```bash
python3 tests/test_automation.py
```

### Mode 5: Launch Streamlit Visual UI
```bash
streamlit run streamlit_app.py
```

### Mode 6: Launch FastAPI Backend
```bash
uvicorn api.app:app --reload --port 8000
```

---

## 📊 Sample Output & Audit Reports

When you run `python3 main.py --mode dry-run`, the terminal displays:

```text
[2026-11-22 16:15:59] [INFO] ======================================================================
[2026-11-22 16:15:59] [INFO] STARTING EMAIL AUTOMATION BATCH RUN [Mode: DRY-RUN SIMULATION]
[2026-11-22 16:15:59] [INFO] ======================================================================
[2026-11-22 16:15:59] [INFO] Loaded 6 scheduled reminder records from CSV database.
[2026-11-22 16:15:59] [INFO] [DRY-RUN SIMULATION] Email to 'Aarav Sharma' <aarav.sharma@example.com> | Subject: 'Live Session Reminder: Python Automation' | MessageID: <179534435947.17715.14569983178148562523@Lohiths-MacBook-Air-2.local>
[2026-11-22 16:15:59] [INFO] [DRY-RUN SIMULATION] Email to 'Priya Patel' <priya.patel@example.com> | Subject: 'Live Session Reminder: Python Automation' | MessageID: <179534435947.17715.2972409509471058698@Lohiths-MacBook-Air-2.local>
[2026-11-22 16:15:59] [INFO] [DRY-RUN SIMULATION] Email to 'Rohan Verma' <rohan.verma@example.com> | Subject: 'Urgent: Invoice Due Notice' | MessageID: <179534435947.17715.5170068252831964812@Lohiths-MacBook-Air-2.local>
[2026-11-22 16:15:59] [INFO] [DRY-RUN SIMULATION] Email to 'Sneha Reddy' <sneha.reddy@example.com> | Subject: 'Webinar Access: Scaling Python Workflows' | MessageID: <179534435947.17715.11124273220296644823@Lohiths-MacBook-Air-2.local>
[2026-11-22 16:15:59] [INFO] [DRY-RUN SIMULATION] Email to 'Ananya Iyer' <ananya.iyer@example.com> | Subject: 'Friendly Notice: Upcoming Bill' | MessageID: <179534435947.17715.763424746848265022@Lohiths-MacBook-Air-2.local>
[2026-11-22 16:15:59] [WARNING] SKIPPED | Contact 'Vikram Malhotra' <vikram.unsub@example.com> has unsubscribed.
[2026-11-22 16:15:59] [INFO] ======================================================================
[2026-11-22 16:15:59] [INFO] BATCH RUN COMPLETED. Audit Report saved to: outputs/delivery_report_20261122_161559.csv
[2026-11-22 16:15:59] [INFO] Summary Metrics: {'total_processed': 6, 'sent_or_simulated': 5, 'failed': 0, 'skipped_unsubscribed': 1, 'success_rate_percent': 83.33}
[2026-11-22 16:15:59] [INFO] ======================================================================
```

### Generated CSV Audit Report (`outputs/delivery_report_*.csv`)
| contact_id | name | email | reminder_type | subject | status | mode | details |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C001 | Aarav Sharma | aarav.sharma@example.com | class_reminder | Live Session Reminder... | simulated_sent | dry_run | Delivered successfully |
| C002 | Priya Patel | priya.patel@example.com | class_reminder | Live Session Reminder... | simulated_sent | dry_run | Delivered successfully |
| C003 | Rohan Verma | rohan.verma@example.com | payment_reminder | Urgent: Invoice Due Notice | simulated_sent | dry_run | Delivered successfully |
| C004 | Sneha Reddy | sneha.reddy@example.com | webinar_alert | Webinar Access... | simulated_sent | dry_run | Delivered successfully |
| C005 | Ananya Iyer | ananya.iyer@example.com | payment_reminder | Friendly Notice: Upcoming Bill | simulated_sent | dry_run | Delivered successfully |
| C006 | Vikram Malhotra | vikram.unsub@example.com | task_reminder | (none) | skipped | (none) | User unsubscribed (opt-out compliance) |

---

## 🎯 Learning Outcomes
- **Relational Data Processing in Python**: Joining multiple CSV datasets and handling missing or malformed fields.
- **Email Protocol Mastery**: Understanding SMTP, TLS encryption handshake, MIME structure (plain text fallback + HTML body), and RFC-compliant message IDs.
- **Enterprise Safety & Reliability**: Implementing dry-run simulators, rate-limit safety, unsubscribe filtering, and error handling.
- **DevOps & Clean Architecture**: Managing environment variables safely with `.gitignore` and `.env.example`.

---

## 📜 License
This project is licensed under the MIT License — feel free to customize and use it for your personal portfolio and academic submissions!
