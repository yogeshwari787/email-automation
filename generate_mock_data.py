"""
generate_mock_data.py
Generates realistic dummy contacts and reminders for high-volume stress testing.
"""
import csv
import random
from pathlib import Path
from src.config import DATA_DIR

FIRST_NAMES = ["Aarav", "Priya", "Rohan", "Sneha", "Ananya", "Vikram", "Neha", "Aditya", "Pooja", "Rahul", "Kavya", "Suresh"]
LAST_NAMES = ["Sharma", "Patel", "Verma", "Reddy", "Iyer", "Malhotra", "Nair", "Mehta", "Chopra", "Gupta", "Deshmukh", "Joshi"]
COMPANIES = ["InnoTech Solutions", "FinEdge Analytics", "CloudScale Systems", "Apex Healthcare", "NextGen Retail", "Tata Consultancy", "Infosys Labs"]
ROLES = ["Software Engineer", "Data Analyst", "DevOps Specialist", "Operations Lead", "HR Manager", "Product Specialist", "QA Engineer"]
COURSES = ["Python Automation Bootcamp", "Advanced Cloud Ops", "HR Analytics & Ops", "Product Operations"]

def generate_mock_dataset(num_records: int = 25):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    contacts = []
    reminders = []

    for i in range(1, num_records + 1):
        cid = f"C{i:03d}"
        rid = f"R{i:03d}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}{i}@example.com"
        company = random.choice(COMPANIES)
        role = random.choice(ROLES)
        course = random.choice(COURSES)
        due_amount = f"{random.randint(0, 500)}.00"
        due_date = f"2026-11-{random.randint(20, 28):02d}"
        unsubscribed = "True" if i % 10 == 0 else "False" # 10% opt-out

        contacts.append({
            "contact_id": cid,
            "name": name,
            "email": email,
            "company": company,
            "role": role,
            "timezone": "Asia/Kolkata",
            "due_amount": due_amount,
            "due_date": due_date,
            "course_name": course,
            "session_time": "7:00 PM IST",
            "unsubscribed": unsubscribed
        })

        rem_type = "class_reminder" if float(due_amount) == 0 else "payment_reminder"
        title = f"Live Session Reminder: {course}" if rem_type == "class_reminder" else "Urgent: Payment Due Notice"

        reminders.append({
            "reminder_id": rid,
            "contact_id": cid,
            "reminder_type": rem_type,
            "title": title,
            "scheduled_time": f"{random.randint(9, 20):02d}:00",
            "recurrence": "DAILY" if rem_type == "class_reminder" else "ONEOFF",
            "active": "True"
        })

    # Save contacts
    contacts_file = DATA_DIR / "contacts.csv"
    with open(contacts_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(contacts[0].keys()))
        writer.writeheader()
        writer.writerows(contacts)

    # Save reminders
    reminders_file = DATA_DIR / "reminders.csv"
    with open(reminders_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(reminders[0].keys()))
        writer.writeheader()
        writer.writerows(reminders)

    print(f"Successfully generated {num_records} realistic test records in {DATA_DIR}!")

if __name__ == "__main__":
    generate_mock_dataset(20)
