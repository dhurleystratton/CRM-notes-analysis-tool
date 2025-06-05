# CRM Notes Analysis Tool

  A Python tool for analyzing chronological CRM note threads to determine engagement status and extract actionable insights.

  ## Overview
  This package processes exported CRM notes as a conversation thread rather than isolated comments. It helps track how deals progress over time and suggests updates
  for your CRM records.

  ## Installation
  Install the dependencies:

  ```bash
  pip install -r requirements.txt

  Usage

  Run the analyzer on a CSV file of CRM notes:

  python analyze_crm_threads.py --input notes.csv --output analysis.json [--company-filter "Acme"]

  Input CSV Columns

  - Item ID
  - Item Name
  - Content Type
  - User
  - Created At
  - Update Content

  The input CSV should include columns like Item ID, Item Name, Content Type, User, Created At and Update Content. The script outputs a JSON file with thread analysis
  and recommended CRM updates.