# Thread analyzer: grouping, chain detection, dispatch to components
from collections import defaultdict
from typing import List, Dict, Any

from .contact_extractor import extract_contacts
from .state_machine import StateMachine


def group_by_thread(notes: List[Dict[str, Any]], key: str = "Item ID") -> Dict[str, List[Dict[str, Any]]]:
    """Group notes by a key (default Item ID)."""
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for note in notes:
        grouped[str(note.get(key, ""))].append(note)
    return grouped


def analyze_thread(notes: List[Dict[str, Any]], state_machine: StateMachine) -> Dict[str, Any]:
    """Analyze a single thread of notes."""
    notes = sorted(notes, key=lambda n: n.get("Created At", ""))
    contacts = set()
    state = state_machine.reset()
    for note in notes:
        text = str(note.get("Update Content", ""))
        contacts.update(extract_contacts(text))
        state = state_machine.transition(text)
    return {
        "final_state": state,
        "contacts": sorted(contacts),
        "notes": notes,
    }


def analyze_threads(notes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze threads of notes and return per-thread report."""
    grouped = group_by_thread(notes)
    sm = StateMachine()
    report = {}
    for thread_id, thread_notes in grouped.items():
        report[thread_id] = analyze_thread(thread_notes, sm)
    return report
