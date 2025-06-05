# CRM Notes Analysis Tool

A Python tool for analyzing chronological CRM note threads to determine engagement status and extract actionable insights.

## Overview
This package processes exported CRM notes as a conversation thread rather than isolated comments. It helps track how deals progress over time and suggests updates for your CRM records.

## Installation
Install the dependencies and the package:

```bash
pip install -r requirements.txt
pip install .
```

## Usage
Run the analyzer on a CSV file of CRM notes:

```bash
python -m crm_notes_analysis_tool.analyze --input notes.csv --output analysis.json
```

The input CSV should include columns like `Item ID`, `Item Name`, `User`, `Created At` and `Update Content`. The script outputs a JSON file with thread analysis and recommended CRM updates.
