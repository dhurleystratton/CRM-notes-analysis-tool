import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any


def parse_notes(csv_path: str) -> List[Dict[str, Any]]:
    """Parse notes CSV into a list of dictionaries."""
    notes = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            notes.append(row)
    return notes


def analyze_notes(notes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Simple analysis that groups notes by item id and returns the last note."""
    threads = defaultdict(list)
    for note in notes:
        threads[note["Item ID"]].append(note)

    results = {}
    for item_id, thread in threads.items():
        # sort by Created At
        thread.sort(key=lambda n: datetime.fromisoformat(n["Created At"]))
        results[item_id] = {
            "item_name": thread[-1]["Item Name"],
            "last_user": thread[-1]["User"],
            "last_content": thread[-1]["Update Content"],
        }
    return results


def analyze_file(input_path: str, output_path: str) -> None:
    """Analyze notes from a CSV file and write JSON output."""
    notes = parse_notes(input_path)
    analysis = analyze_notes(notes)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze CRM note threads")
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--output", required=True, help="Output JSON file")
    args = parser.parse_args()
    analyze_file(args.input, args.output)
