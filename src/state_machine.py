"""Simple keyword-based state machine for CRM thread analysis."""

from typing import Optional


class StateMachine:
    def __init__(self):
        self.state = "start"

    def reset(self) -> str:
        self.state = "start"
        return self.state

    def transition(self, text: str) -> str:
        lower = text.lower()
        if "meeting" in lower or "call" in lower:
            self.state = "engaged"
        if "signed" in lower or "won" in lower:
            self.state = "closed_won"
        if "lost" in lower or "no longer interested" in lower:
            self.state = "closed_lost"
        return self.state
