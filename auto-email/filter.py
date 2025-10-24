import argparse
import re
import sys
import pandas as pd

from rich import print

REQUIRED_FIELDS = ['company_name', 'contact_name', 'email', 'usdot', 'form_path', 'invoice_path']
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'


def load_csv(path):
    """Loads a CSV file into a DataFrame, skipping malformed rows."""
    try:
        df = pd.read_csv(path, dtype=str, on_bad_lines='skip')

        # Drop leftover index column from previous export, if exists
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])

        missing_cols = [col for col in REQUIRED_FIELDS if col not in df.columns]
        if missing_cols:
            sys.exit(f"Missing required columns in CSV: {missing_cols}")

        return df
    except Exception as e:
        sys.exit(f"Error loading CSV: {e}")

def is_valid_email(email):
    """Validates the email using regex."""
    return re.match(EMAIL_REGEX, str(email)) is not None


def basic_filter(df):
    """Removes rows with missing/empty required fields, strip whitespace."""
    df = df.dropna(subset=REQUIRED_FIELDS).loc[
        lambda d: ~d[REQUIRED_FIELDS].apply(lambda x: x.astype(str).str.strip() == "").any(axis=1)
    ]
    df = df.map(lambda x: str(x).replace('\n', ' ').replace('\r', ' '))
    return df


def advanced_filter(df):
    """Removes rows with invalid email formats."""
    return df[df['email'].apply(is_valid_email)]


def filter_data(df, verbose=False):
    """Applies all filters in order."""
    original_count = len(df)

    df = basic_filter(df)
    after_basic = len(df)

    df = advanced_filter(df)
    after_advanced = len(df)

    if verbose:
        print(f"Original entries: {original_count}")
        print(f"After basic filtering: {after_basic}")
        print(f"After advanced filtering (email): {after_advanced}")
        print(f"Total removed: {original_count - after_advanced}")

    return df

def term_parse():
    parser = argparse.ArgumentParser(description="Filter CSV data based on field presence and email validity.")
    parser.add_argument("input_csv", help="Path to the input CSV file.")
    parser.add_argument("output_csv", help="Path to save the filtered CSV file.")
    parser.add_argument("--verbose", action="store_true", help="Print filtering statistics.")
    return parser.parse_args()

def main():
    args = term_parse()

    df = load_csv(args.input_csv)
    filtered_df = filter_data(df, verbose=args.verbose)
    filtered_df.to_csv(args.output_csv, index=False)

    if args.verbose:
        print(f"Filtered data saved to: {args.output_csv}")


if __name__ == "__main__":
    main()
