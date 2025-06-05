import argparse
import csv
import json
import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta


# Constants
DATE_FORMAT = "%d/%B/%Y %I:%M:%S %p"
CHAIN_GAP_DAYS = 30
STALE_DAYS = 180

POSITIVE_WORDS = ["interested", "discussing", "considering", "would like"]
NEGATIVE_WORDS = ["not interested", "declined", "pass"]
TEMPORAL_WORDS = ["not right now", "maybe later", "revisit"]

STATES = [
    "INITIAL_OUTREACH",
    "RESPONDED",
    "DISCUSSING",
    "INTERESTED",
    "NEGOTIATING",
    "CLOSED_WON",
    "CLOSED_LOST",
    "NO_RESPONSE",
    "FOLLOW_UP",
    "RE_ENGAGED",
]

def progress_bar(iterable, label="Processing"):
    total = len(iterable)
    width = 40
    for i, item in enumerate(iterable, 1):
        done = width * i // total if total else width
        bar = "#" * done + "." * (width - done)
        percent = (100 * i // total) if total else 100
        print(f"\r{label}: [{bar}] {percent}% ({i}/{total})", end="", flush=True)
        yield item
    print()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Analyze CRM note threads")
    parser.add_argument("--input", required=True, help="Path to notes CSV")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    parser.add_argument("--company-filter", help="Only process company names containing this string")
    return parser.parse_args()


def load_data(csv_path, company_filter=None):
    groups = defaultdict(list)
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if company_filter and company_filter.lower() not in row["Item Name"].lower():
                continue
            groups[row["Item ID"]].append(row)
    return groups


def parse_date(text):
    return datetime.strptime(text, DATE_FORMAT)


def extract_contacts(text):
    contacts = []
    email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    name_title_pattern = re.compile(r"([A-Z][a-z]+ [A-Z][a-z]+)\s*\(([^)]+)\)")
    spoke_with_pattern = re.compile(r"spoke with ([A-Z][a-z]+ [A-Z][a-z]+)", re.IGNORECASE)
    for match in name_title_pattern.finditer(text):
        name, title = match.groups()
        contacts.append({"name": name, "title": title, "email": None})
    for match in spoke_with_pattern.finditer(text):
        name = match.group(1)
        contacts.append({"name": name, "title": None, "email": None})
    for match in email_pattern.finditer(text):
        contacts.append({"name": None, "title": None, "email": match.group(0)})
    return contacts


def update_state(current_state, text):
    tl = text.lower()
    if "do not contact" in tl:
        return "CLOSED_LOST", "do not contact"
    for word in NEGATIVE_WORDS:
        if word in tl:
            return "CLOSED_LOST", word
    if "closed won" in tl:
        return "CLOSED_WON", "closed won"
    if "negotiating" in tl:
        return "NEGOTIATING", "negotiating"
    for word in POSITIVE_WORDS:
        if word in tl:
            return "INTERESTED", word
    if "discuss" in tl or "meeting" in tl:
        return "DISCUSSING", "discussing"
    if "responded" in tl or "replied" in tl:
        return "RESPONDED", "responded"
    if "follow up" in tl or "following up" in tl:
        return "FOLLOW_UP", "follow up"
    if current_state == "NO_RESPONSE" and "reached out" in tl:
        return "RE_ENGAGED", "re-engaged"
    return current_state, None


def analyze_company(item_id, company_name, rows):
    rows.sort(key=lambda r: parse_date(r["Created At"]))
    chains = []
    chain = []
    last_date = None
    contacts = {}
    state = "INITIAL_OUTREACH"
    progression = []

    for row in rows:
        note_date = parse_date(row["Created At"])
        if last_date and (note_date - last_date).days > CHAIN_GAP_DAYS:
            chains.append(chain)
            chain = []
        chain.append(row)
        last_date = note_date

        extracted = extract_contacts(row["Update Content"])
        for c in extracted:
            key = (c["name"], c["email"])
            if key not in contacts:
                contacts[key] = {
                    "name": c["name"],
                    "title": c["title"],
                    "email": c["email"],
                    "first_mentioned": note_date.strftime("%Y-%m-%d"),
                }
        new_state, reason = update_state(state, row["Update Content"])
        if new_state != state and reason:
            state = new_state
            progression.append({
                "date": note_date.strftime("%Y-%m-%d"),
                "state": state,
                "reason": reason,
            })
    if chain:
        chains.append(chain)

    date_range = (
        parse_date(rows[0]["Created At"]),
        parse_date(rows[-1]["Created At"]),
    )
    final_state = state
    if (datetime.now() - date_range[1]).days > STALE_DAYS:
        final_state = "STALE"

    summary = {
        "item_id": item_id,
        "company_name": company_name,
        "thread_analysis": {
            "total_notes": len(rows),
            "date_range": f"{date_range[0].date()} - {date_range[1].date()}",
            "conversation_chains": len(chains),
            "final_state": final_state,
            "progression": progression,
        },
        "contacts_discovered": list(contacts.values()),
        "recommended_updates": {
            "status": final_state,
            "confidence": 0.95,
            "reasoning": progression[-1]["reason"] if progression else "",
            "new_contacts_to_add": [c for c in contacts.values() if c["email"]],
            "do_not_contact": [c for c in contacts.values() if c["title"] and "do not contact" in c["title"].lower()],
        },
    }
    return summary


def main():
    args = parse_args()
    groups = load_data(args.input, args.company_filter)

    results = []
    mismatches = 0
    high_value = 0
    logging.info("Processing %d companies", len(groups))
    for item_id, rows in progress_bar(list(groups.items()), label="Analyzing"):
        company_name = rows[0]["Item Name"]
        result = analyze_company(item_id, company_name, rows)
        results.append(result)
        if result["thread_analysis"]["final_state"] == "CLOSED_LOST":
            last_note = parse_date(rows[-1]["Created At"])
            if (datetime.now() - last_note).days < 60:
                mismatches += 1
        if len(result["contacts_discovered"]) > 1 and result["thread_analysis"]["final_state"] in ["INTERESTED", "NEGOTIATING"]:
            high_value += 1

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    logging.info("Summary: %d companies processed", len(results))
    logging.info("Status mismatches: %d", mismatches)
    logging.info("High value opportunities: %d", high_value)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("Failed: %s", e)
