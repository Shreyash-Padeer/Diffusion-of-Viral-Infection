import csv
import argparse
import os

def convert_txt_to_csv(input_txt_path, output_csv_path):
    """
    Reads a space-separated TXT file (node1 node2 probability) and
    writes it to a CSV file with a header. Skips lines starting with '#'.

    Args:
        input_txt_path (str): Path to the input TXT file.
        output_csv_path (str): Path where the output CSV file will be saved.
    """
    header = ['source_node', 'target_node', 'probability']
    rows_written = 0

    try:
        with open(input_txt_path, 'r') as infile, \
             open(output_csv_path, 'w', newline='') as outfile: # Use newline='' for csv writer

            writer = csv.writer(outfile)

            # Write the header
            writer.writerow(header)

            # Read the input file line by line
            for line in infile:
                # Remove leading/trailing whitespace
                line = line.strip()

                # Skip empty lines and comment lines
                if not line or line.startswith('#'):
                    continue

                # Split the line into parts based on whitespace
                parts = line.split()

                # Ensure we have exactly 3 parts
                if len(parts) == 3:
                    # Write the parts as a row in the CSV
                    writer.writerow(parts)
                    rows_written += 1
                else:
                    print(f"Warning: Skipping malformed line: '{line}'")

        print(f"Successfully converted '{input_txt_path}' to '{output_csv_path}'.")
        print(f"Wrote {rows_written} data rows.")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_txt_path}'")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    # Set up argument parser for command-line usage
    parser = argparse.ArgumentParser(
        description="Convert space-separated node/probability TXT file to CSV."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input TXT file (e.g., dataset_funnel_v5.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional: Path for the output CSV file. Defaults to input filename with .csv extension."
    )

    args = parser.parse_args()

    # Determine the output filename if not provided
    if args.output:
        output_filename = args.output
    else:
        # Replace .txt extension with .csv, or append .csv if no extension
        base = os.path.splitext(args.input_file)[0]
        output_filename = base + ".csv"

    # Run the conversion function
    convert_txt_to_csv(args.input_file, output_filename)