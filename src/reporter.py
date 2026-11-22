"""
src/reporter.py
Generates CSV audit reports and execution statistics for automated emails.
Works with both Pandas and standard library csv module.
"""
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import csv
from .config import OUTPUTS_DIR

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class ExecutionReporter:
    def __init__(self, output_dir: Path = OUTPUTS_DIR):
        self.output_dir = output_dir

    def save_report(self, records: List[Dict[str, Any]], filename_prefix: str = "delivery_report") -> Path:
        """
        Saves the results of an email dispatch run into a timestamped CSV report.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"{filename_prefix}_{timestamp}.csv"

        if HAS_PANDAS:
            df = pd.DataFrame(records)
            df.to_csv(report_path, index=False)
        else:
            if records:
                keys = list(records[0].keys())
                with open(report_path, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(records)

        return report_path

    @staticmethod
    def generate_summary(records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates success rate, failure counts, and skips."""
        total = len(records)
        sent = sum(1 for r in records if r.get("status") in ("sent", "simulated_sent"))
        failed = sum(1 for r in records if r.get("status") == "failed")
        skipped = sum(1 for r in records if r.get("status") == "skipped")
        rate = (sent / total * 100) if total > 0 else 0.0

        return {
            "total_processed": total,
            "sent_or_simulated": sent,
            "failed": failed,
            "skipped_unsubscribed": skipped,
            "success_rate_percent": round(rate, 2)
        }
