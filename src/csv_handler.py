"""
src/csv_handler.py
Handles reading, validating, and managing contacts and reminders CSV files.
Supports both Pandas and Python's built-in csv module.
"""
from pathlib import Path
from typing import List, Dict, Any
import csv
from .config import DATA_DIR

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class CSVHandler:
    @staticmethod
    def load_contacts(file_path: Path = DATA_DIR / "contacts.csv") -> List[Dict[str, Any]]:
        """Loads contacts from CSV and returns list of valid contact dicts."""
        if not file_path.exists():
            raise FileNotFoundError(f"Contacts file not found at: {file_path}")

        if HAS_PANDAS:
            df = pd.read_csv(file_path, dtype=str)
            df.fillna("", inplace=True)
            if "unsubscribed" in df.columns:
                df["unsubscribed"] = df["unsubscribed"].astype(str).str.lower().isin(["true", "1", "yes"])
            else:
                df["unsubscribed"] = False
            return df.to_dict(orient="records")
        else:
            records = []
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned = {k.strip(): v.strip() for k, v in row.items()}
                    cleaned["unsubscribed"] = cleaned.get("unsubscribed", "").lower() in ("true", "1", "yes")
                    records.append(cleaned)
            return records

    @staticmethod
    def load_reminders(file_path: Path = DATA_DIR / "reminders.csv") -> List[Dict[str, Any]]:
        """Loads scheduled reminder records."""
        if not file_path.exists():
            raise FileNotFoundError(f"Reminders file not found at: {file_path}")

        if HAS_PANDAS:
            df = pd.read_csv(file_path, dtype=str)
            df.fillna("", inplace=True)
            if "active" in df.columns:
                df["active"] = df["active"].astype(str).str.lower().isin(["true", "1", "yes"])
            else:
                df["active"] = True
            return df.to_dict(orient="records")
        else:
            records = []
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned = {k.strip(): v.strip() for k, v in row.items()}
                    cleaned["active"] = cleaned.get("active", "true").lower() in ("true", "1", "yes")
                    records.append(cleaned)
            return records

    @staticmethod
    def merge_contacts_and_reminders(
        contacts_file: Path = DATA_DIR / "contacts.csv",
        reminders_file: Path = DATA_DIR / "reminders.csv"
    ) -> List[Dict[str, Any]]:
        """Performs inner join between reminders and contacts on contact_id."""
        contacts = CSVHandler.load_contacts(contacts_file)
        reminders = CSVHandler.load_reminders(reminders_file)

        contacts_by_id = {c["contact_id"]: c for c in contacts if "contact_id" in c}
        merged = []
        for rem in reminders:
            cid = rem.get("contact_id")
            if cid in contacts_by_id:
                combined = {**contacts_by_id[cid], **rem}
                merged.append(combined)
        return merged
