import argparse

from mcs150.load import load_companies_from_forms
from log import log 

def term_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", help="Path to the output CSV.")
    parser.add_argument("--mcs150_dir", help="Directory of MCS-150 forms that will be used for extracting emails.")
    parser.add_argument("--invoices_dir", help="Directory of invoices that will be sent alongside MCS-150 forms.")
    return parser.parse_args()

def main():
    args = term_parse()

    try:
        df = load_companies_from_forms(args.mcs150_dir, args.invoices_dir)
        log.info(f"Using MCS-150 dir at: '{args.mcs150_dir}'.")
        log.info(f"Using invoices dir at: '{args.invoices_dir}'.")
        log.info(f"Saving extracted data to csv at: '{args.csv_path}'")
        df.to_csv(args.csv_path)
    except Exception as e:
        log.error(f"Error saving companies data to '{args.csv_path}': {e}.")


if __name__ == "__main__":
    main()