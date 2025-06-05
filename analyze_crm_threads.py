 #!/usr/bin/env python3
  """CRM Notes Thread Analysis Tool - Main CLI Entry Point

  This tool analyzes CRM note threads to understand conversation progression
  and generate dataset updates for the Liberation Day tariff settlement project.
  """

  import argparse
  import csv
  import json
  import logging
  from pathlib import Path
  import sys
  from typing import Dict, List, Optional

  from src.thread_analyzer import ThreadAnalyzer
  from src.state_machine import ConversationStateMachine
  from src.contact_extractor import ContactExtractor
  from src.report_generator import ReportGenerator

  # Configure logging
  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  )
  logger = logging.getLogger(__name__)


  def parse_args():
      """Parse command line arguments."""
      parser = argparse.ArgumentParser(
          description="Analyze CRM note threads to understand conversation progression",
          epilog="Example: python analyze_crm_threads.py --input notes.csv --output analysis.json"
      )
      parser.add_argument(
          "--input",
          required=True,
          type=str,
          help="Path to input CSV file with CRM notes"
      )
      parser.add_argument(
          "--output",
          required=True,
          type=str,
          help="Path to output JSON file for analysis results"
      )
      parser.add_argument(
          "--company-filter",
          type=str,
          help="Optional: Only process companies containing this string"
      )
      parser.add_argument(
          "--verbose",
          action="store_true",
          help="Enable verbose logging"
      )
      return parser.parse_args()


  def load_notes(csv_path: str, company_filter: Optional[str] = None) -> List[Dict]:
      """Load notes from CSV file with optional company filtering."""
      notes = []
      try:
          with open(csv_path, newline="", encoding="utf-8") as f:
              reader = csv.DictReader(f)

              # Validate required columns
              required_columns = {"Item ID", "Item Name", "Content Type", "User", "Created At", "Update Content"}
              if not required_columns.issubset(reader.fieldnames):
                  missing = required_columns - set(reader.fieldnames)
                  raise ValueError(f"Missing required columns: {missing}")

              for row in reader:
                  # Apply company filter if specified
                  if company_filter and company_filter.lower() not in row["Item Name"].lower():
                      continue
                  notes.append(row)

          logger.info(f"Loaded {len(notes)} notes from {csv_path}")
          return notes

      except FileNotFoundError:
          logger.error(f"Input file not found: {csv_path}")
          sys.exit(1)
      except Exception as e:
          logger.error(f"Error loading CSV: {e}")
          sys.exit(1)


  def main():
      """Main entry point for the CRM thread analysis tool."""
      args = parse_args()

      if args.verbose:
          logging.getLogger().setLevel(logging.DEBUG)

      logger.info("Starting CRM thread analysis...")

      # Load notes from CSV
      notes = load_notes(args.input, args.company_filter)

      if not notes:
          logger.warning("No notes found matching criteria")
          sys.exit(0)

      # Initialize components
      thread_analyzer = ThreadAnalyzer()
      state_machine = ConversationStateMachine()
      contact_extractor = ContactExtractor()
      report_generator = ReportGenerator()

      # Analyze threads
      logger.info("Analyzing conversation threads...")
      threads = thread_analyzer.analyze_threads(notes)

      # Process each thread through state machine
      logger.info(f"Processing {len(threads)} company threads...")
      for thread in threads.values():
          # Extract contacts from all notes in thread
          thread["contacts"] = contact_extractor.extract_from_thread(thread["notes"])

          # Analyze conversation state progression
          thread["state_analysis"] = state_machine.analyze_progression(thread["notes"])

      # Generate report
      logger.info("Generating analysis report...")
      report = report_generator.generate_report(threads)

      # Write output
      output_path = Path(args.output)
      output_path.parent.mkdir(parents=True, exist_ok=True)

      with open(output_path, 'w', encoding='utf-8') as f:
          json.dump(report, f, indent=2, ensure_ascii=False)

      logger.info(f"Analysis complete. Results written to {args.output}")

      # Print summary statistics
      print("\n=== Analysis Summary ===")
      print(f"Total companies analyzed: {len(threads)}")
      print(f"Total notes processed: {len(notes)}")

      # Count final states
      state_counts = {}
      for company in report:
          final_state = company["thread_analysis"]["final_state"]
          state_counts[final_state] = state_counts.get(final_state, 0) + 1

      print("\nFinal state distribution:")
      for state, count in sorted(state_counts.items()):
          print(f"  {state}: {count}")

      # Identify high-value opportunities
      high_value = [
          c for c in report
          if len(c["contacts_discovered"]) > 1
          and c["thread_analysis"]["final_state"] in ["INTERESTED", "NEGOTIATING", "DISCUSSING"]
      ]
      print(f"\nHigh-value opportunities: {len(high_value)}")

      # Identify stale conversations
      stale = [c for c in report if c["thread_analysis"]["final_state"] == "STALE"]
      print(f"Stale conversations (>6 months): {len(stale)}")

      # Identify do-not-contact
      dnc = [c for c in report if c["recommended_updates"].get("do_not_contact")]
      print(f"Do-not-contact companies: {len(dnc)}")


  if __name__ == "__main__":
      try:
          main()
      except KeyboardInterrupt:
          logger.info("Analysis interrupted by user")
          sys.exit(1)
      except Exception as e:
          logger.exception(f"Unexpected error: {e}")
          sys.exit(1)

