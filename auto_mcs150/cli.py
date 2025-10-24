import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(prog="AutoMCS150", description="Script for automated bulk filling of MCS-150 forms.")
    parser.add_argument("usdots_path",help="Path to a .csv file containing the USDOT numbers to be processed.")
    parser.add_argument("--usdot_column", default=None, help="The name of the column containing usdots in the .csv provided.")
    parser.add_argument("--output_dir", default=None, help="Output directory for the filled-out forms.")
    parser.add_argument("--path_to_mcs150_template", default=None, help="Path to the MCS-150 form template.")
    parser.add_argument("--before", default=None, help="Include only companies that updated their MCS-150 before the given date.")
    parser.add_argument("--accept_out_of_service", action="store_true", default=False, help="Accept companies that are out of service. False by default.")
    parser.add_argument('--max_retries', type=int, default=0, help='Max retries in case of SSLError (default: 0)')
    parser.add_argument('--time_before_retry', type=int, default=0, help='Seconds to wait before retrying (default: 0)')
    parser.add_argument('--spreadsheet_path', default=None, help="Path to the spreadsheet used for appending company contact info (eg. email) to a form.")

    return parser.parse_args()