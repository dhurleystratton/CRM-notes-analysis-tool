codex/refactor-analyze_crm_threads-into-modules
"""Lightweight CLI for CRM notes thread analysis."""

import argparse
import csv
from pathlib import Path

from src.thread_analyzer import analyze_threads
from src.report_generator import generate_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze CRM note threads")
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--output", help="Output JSON file")
    args = parser.parse_args()

    notes = []
    with open(args.input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            notes.append(row)

    threads = analyze_threads(notes)
    report = generate_report(threads)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()