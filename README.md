# CRM-notes-analysis-tool
Python tool that analyzes CRM note threads to understand conversation progression and generate dataset updates. The tool must process chronological notes for each company and determine the final state of engagement.

  Just include a simple overview - don't paste all the technical details. Here's what the README should contain:

  # CRM Notes Analysis Tool

  A Python tool for analyzing conversation threads in CRM note exports to determine engagement status and extract actionable insights.

  ## Overview
  This tool processes chronological CRM notes to understand conversation progression rather than treating each note in isolation. It tracks how sales conversations evolve over time and provides recommendations for updating CRM records.

  ## Installation
  ```bash
  pip install -r requirements.txt

  Usage

  python analyze_crm_threads.py --input notes.csv --output analysis.json

  Input Format

  Expects CSV with columns: Item ID, Item Name, User, Created At, Update Content

  Output

  JSON file with thread analysis, discovered contacts, and recommended CRM updates.

## Testing
Run the test suite with:
```bash
python -m unittest discover
```
or using pytest:
```bash
pytest
```
