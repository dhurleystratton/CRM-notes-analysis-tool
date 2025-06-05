# CRM Notes Analysis Tool

A lightweight Python script for analyzing CRM note threads. It groups notes by company, tracks conversation progression, extracts contacts, and produces a JSON report summarizing engagement.

## Usage

```bash
python analyze_crm_threads.py --input notes.csv --output analysis.json [--company-filter "Acme"]
```

### Input CSV Columns
- Item ID
- Item Name
- Content Type
- User
- Created At
- Update Content

The output JSON includes thread statistics, contact information, and recommended status updates for each company.
