import json5
import os

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:

    @staticmethod
    def load_json(path):
        with open(path) as f:
            return json5.load(f)
    
    passwords = load_json(f"{MODULE_DIR}/.password.jsonc")
    email_accounts = passwords.keys()
   
    spreadsheet = f"{MODULE_DIR}/companies.csv"
    sheet_to_df_map = load_json(f"{MODULE_DIR}/sheet_to_df_map.jsonc")

    mcs150_dir = "/home/meow/work/MCS-150 forms/en/October"
    invoices_dir = "/home/meow/work/invoices/en/October"
    companies_csv_path = f"{MODULE_DIR}/data/filtered_companies.csv"

    max_emails = 20
    companies_sent_file = f"{MODULE_DIR}/data/companies_sent.txt"

    EMAILS_BOOLMAP_PATH = f"{MODULE_DIR}/data/emails_validity.jsonc"
    emails_boolmap = load_json(EMAILS_BOOLMAP_PATH)

    test_mcs150_dir = "/home/meow/work/scripts/test/mcs150"
    test_invoices_dir = "/home/meow/work/scripts/test/invoices"
