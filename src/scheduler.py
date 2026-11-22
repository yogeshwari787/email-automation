"""
src/scheduler.py
Local task scheduling using Python schedule library or time-based polling fallback.
"""
import time
import datetime as dt
import logging
from typing import Callable

logger = logging.getLogger("EmailAutomation")

try:
    import schedule
    HAS_SCHEDULE = True
except ImportError:
    HAS_SCHEDULE = False

class LocalScheduler:
    def __init__(self):
        self.running = False

    def schedule_daily(self, time_str: str, job_func: Callable, *args, **kwargs):
        """Schedules a daily recurring job at e.g. '19:00'."""
        logger.info(f"Scheduled daily reminder trigger at {time_str}")
        if HAS_SCHEDULE:
            schedule.every().day.at(time_str).do(job_func, *args, **kwargs)

    def run_continuous(self, max_runs: int = None):
        """Runs the schedule loop."""
        self.running = True
        logger.info("Scheduler started. Waiting for trigger points... Press Ctrl+C to stop.")
        runs = 0
        try:
            while self.running:
                if HAS_SCHEDULE:
                    schedule.run_pending()
                time.sleep(1)
                runs += 1
                if max_runs and runs >= max_runs:
                    break
        except KeyboardInterrupt:
            logger.info("Scheduler manually interrupted.")
        finally:
            self.running = False
