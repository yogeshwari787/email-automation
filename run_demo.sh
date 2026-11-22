#!/usr/bin/env bash
# ==============================================================================
# One-Click Project Demo Runner for Email Automation & Reminder System
# ==============================================================================

set -e

echo ""
echo "======================================================================"
echo "🚀 EMAIL AUTOMATION & REMINDER SYSTEM - AUTOMATED DEMO"
echo "======================================================================"
echo ""

# 1. Run Automated Tests
echo "▶️ Step 1: Running Automated Test Suite..."
python3 tests/test_automation.py
echo ""

# 2. Run Synthetic Mock Generator
echo "▶️ Step 2: Generating Fresh Mock Data (20 records)..."
python3 generate_mock_data.py
echo ""

# 3. Execute Automation Batch (Dry-Run Mode)
echo "▶️ Step 3: Executing Email Automation Engine (Safe Dry-Run)..."
python3 main.py --mode dry-run
echo ""

# 4. Display the Generated Audit Report
echo "▶️ Step 4: Displaying Latest CSV Delivery Report (outputs/)..."
LATEST_REPORT=$(ls -t outputs/delivery_report_*.csv | head -1)
echo "Report file: $LATEST_REPORT"
echo "----------------------------------------------------------------------"
head -n 7 "$LATEST_REPORT"
echo "----------------------------------------------------------------------"
echo ""

echo "======================================================================"
echo "✅ DEMO EXECUTION COMPLETE! System is 100% operational."
echo "======================================================================"
