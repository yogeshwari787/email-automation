"""
streamlit_app.py
Interactive Web Dashboard for Email Automation & Reminder System.
Allows users to view contacts, test email templates, trigger automation batches,
and inspect real-time delivery logs and analytics without needing Node.js/Next.js.
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from src.config import config, DATA_DIR, LOGS_DIR, OUTPUTS_DIR
from src.csv_handler import CSVHandler
from src.renderer import EmailRenderer
from src.mailer import EmailSender
from main import execute_automation_batch

st.set_page_config(
    page_title="Email Automation & Reminder Dashboard",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Email Automation & Reminder Dashboard")
st.markdown("Automated notifications, reminders, delivery logs, and campaign audit reports.")

tabs = st.tabs(["📊 Overview & Trigger", "👥 Contacts & Reminders", "📝 Template Preview", "📜 Audit Logs & Reports"])

with tabs[0]:
    st.subheader("System Control & Quick Dispatch")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mode", "DRY-RUN (Safe Simulation)" if config.DRY_RUN else "LIVE SMTP")
    with col2:
        st.metric("Default Timezone", config.TIMEZONE)
    with col3:
        st.metric("Sender Account", config.SENDER_EMAIL)

    st.markdown("---")
    st.write("Trigger batch dispatch of all scheduled reminder emails:")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 Run Dry-Run Simulation Now", type="primary"):
            with st.spinner("Processing contacts and personalizing messages..."):
                report_file, summary = execute_automation_batch(dry_run=True)
                st.success(f"Batch completed successfully! Generated report: {report_file.name}")
                st.json(summary)
    with col_btn2:
        if st.button("⚠️ Run Live SMTP Send (Uses Real Credentials)"):
            with st.spinner("Connecting to SMTP server and dispatching..."):
                report_file, summary = execute_automation_batch(dry_run=False)
                st.info(f"Live batch completed! Report: {report_file.name}")
                st.json(summary)

with tabs[1]:
    st.subheader("Contacts & Reminder Records")
    try:
        contacts_df = pd.read_csv(DATA_DIR / "contacts.csv")
        reminders_df = pd.read_csv(DATA_DIR / "reminders.csv")
        st.markdown("**Registered Contacts (`contacts.csv`)**")
        st.dataframe(contacts_df, use_container_width=True)
        st.markdown("**Scheduled Reminders (`reminders.csv`)**")
        st.dataframe(reminders_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading CSV files: {e}")

with tabs[2]:
    st.subheader("Dynamic Email Personalization Preview")
    renderer = EmailRenderer()
    sample_context = {
        "name": "Aarav Sharma",
        "company": "InnoTech Solutions",
        "role": "Software Engineer",
        "course_name": "Python Automation Bootcamp",
        "session_time": "7:00 PM IST",
        "timezone": "Asia/Kolkata",
        "due_amount": "150.00",
        "due_date": "2026-11-25",
        "contact_id": "C001"
    }
    
    template_choice = st.selectbox("Select Template", ["reminder_template.html", "payment_reminder.html"])
    rendered_html = renderer.render_template(template_choice, sample_context)
    st.markdown("### Rendered Output Preview")
    st.components.v1.html(rendered_html, height=500, scrolling=True)

with tabs[3]:
    st.subheader("Audit Logs & Delivery Reports")
    log_file = LOGS_DIR / "email_automation.log"
    if log_file.exists():
        st.markdown("**Recent System Logs (`logs/email_automation.log`)**")
        with open(log_file, "r") as f:
            lines = f.readlines()[-40:]
            st.code("".join(lines), language="text")

    reports = sorted(list(OUTPUTS_DIR.glob("delivery_report_*.csv")), reverse=True)
    if reports:
        st.markdown("**Latest Generated Delivery Report**")
        latest_report = pd.read_csv(reports[0])
        st.dataframe(latest_report, use_container_width=True)
