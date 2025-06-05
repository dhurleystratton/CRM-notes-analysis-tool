import click

@click.command()
@click.option('--input', 'input_path', required=True, help='CSV file of CRM notes')
@click.option('--output', 'output_path', required=True, help='Where to write the analysis JSON')
def main(input_path: str, output_path: str) -> None:
    """Placeholder analysis command."""
    # In a real implementation, analyze the notes here.
    click.echo(f"Analyzing {input_path} -> {output_path}")

if __name__ == '__main__':
    main()
