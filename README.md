# CRM-notes-analysis-tool
Python tool that analyzes CRM note threads to understand conversation progression and generate dataset updates. The tool must process chronological notes for each company and determine the final state of engagement.

  CONTEXT:
  - Input: CSV file with columns: Item ID, Item Name, Content Type, User, Created At, Update Content
  - Notes are chronological updates about sales conversations with companies
  - Multiple notes per company form conversation threads
  - Need to understand progression, not just individual notes

  REQUIREMENTS:
  1. THREAD ANALYSIS ENGINE:
  - Group notes by Item ID (company identifier)
  - Sort by Created At timestamp (format: "DD/Month/YYYY HH:MM:SS AM/PM")
  - Identify conversation chains (related notes within 30 days)
  - Detect conversation restarts (gaps > 30 days)

  2. STATE MACHINE:
  Create states: INITIAL_OUTREACH -> RESPONDED -> DISCUSSING -> INTERESTED -> NEGOTIATING -> CLOSED_WON -> CLOSED_LOST
  Also handle: NO_RESPONSE -> FOLLOW_UP -> RE_ENGAGED
  Track state transitions with dates and reasons

  3. CONTACT EXTRACTION:
  - Extract names from patterns like "spoke with John Smith" or "John Smith (CFO)"
  - Extract emails from text
  - Extract titles from "Name (Title)" or "Title: Name" patterns
  - Track when conversations escalate to new contacts

  4. SENTIMENT ANALYSIS:
  Positive indicators: "interested", "discussing", "considering", "would like"
  Negative indicators: "not interested", "declined", "pass"
  Temporal qualifiers: "not right now", "maybe later", "revisit in Q3"

  5. OUTPUT GENERATOR:
  For each company, output JSON with:
  {
    "item_id": "xxx",
    "company_name": "xxx",
    "thread_analysis": {
      "total_notes": N,
      "date_range": "start - end",
      "conversation_chains": N,
      "final_state": "STATE",
      "progression": [
        {"date": "xxx", "state": "xxx", "reason": "xxx"}
      ]
    },
    "contacts_discovered": [
      {"name": "xxx", "title": "xxx", "email": "xxx", "first_mentioned": "date"}
    ],
    "recommended_updates": {
      "status": "xxx",
      "confidence": 0.95,
      "reasoning": "xxx",
      "new_contacts_to_add": [],
      "do_not_contact": []
    }
  }

  6. SPECIAL CASES:
  - If latest note is >6 months old, mark as "STALE"
  - If "do not contact" appears, override all other signals
  - If forwarded to new person, track both contacts
  - If company says "not interested" but later re-engages, update to current state

  7. CLI INTERFACE:
  python analyze_crm_threads.py --input notes.csv --output analysis.json --company-filter "optional"

  8. BATCH PROCESSING:
  - Process all companies and generate summary statistics
  - Identify companies with status mismatches (e.g., marked "Not Interested" but showing engagement)
  - Flag high-value opportunities (multiple engaged contacts, recent activity)

  Include comprehensive error handling, logging, and progress bars for large datasets.
