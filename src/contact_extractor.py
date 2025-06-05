"""Utilities for extracting contact info from text."""

import re
from typing import List, Set

EMAIL_RE = re.compile(r"[\w.-]+@[\w.-]+\.[A-Za-z]+")
PHONE_RE = re.compile(r"\+?\d[\d -]{7,}\d")


def extract_contacts(text: str) -> Set[str]:
    """Return set of discovered emails and phone numbers."""
    emails = set(EMAIL_RE.findall(text))
    phones = set(PHONE_RE.findall(text))
    return emails.union(phones)
