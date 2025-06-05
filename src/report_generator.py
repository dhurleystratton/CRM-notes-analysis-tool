"""Generate JSON report and summary statistics."""

import json
from typing import Dict, Any


def generate_report(thread_data: Dict[str, Any]) -> str:
    """Return JSON string with analysis report and summary stats."""
    summary = {
        "total_threads": len(thread_data),
        "states": {},
        "contacts_found": 0,
    }
    for info in thread_data.values():
        state = info["final_state"]
        summary["states"][state] = summary["states"].get(state, 0) + 1
        summary["contacts_found"] += len(info["contacts"])

    payload = {
        "summary": summary,
        "threads": thread_data,
    }
    return json.dumps(payload, indent=2)
