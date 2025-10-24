import pandas as pd

import random
import time

from mcs150.send import send_mcs150_and_invoice
from mcs150.load import load_companies_from_forms
from utils import is_inside_dir, load_str_list, save_str_list
from log import log
from config import Config


def process_companies(companies: pd.DataFrame, max_emails, email_login, email_password, ignore_list=None, emails_boolmap=None, delay: float = 5, jitter=0.5) -> set:
    """
    Iterates through a DataFrame of companies and sends each their messages,
    form and invoice via email.
    
    Parameters:
        companies (pd.DataFrame): DataFrame with company info.
        delay (float): Base delay between emails in seconds.
        max_emails (int): Stop after sending this many emails.
        jitter (float): Proportion of delay to randomize (e.g., 0.3 = ±30%).
        ignore_list (list[str]): List of company usdots to ignore
        emails_boolmap (list[str]): A map of emails and their states, True for valid and False for invalid

    Returns:
        companies_sent (set): set of company usdots that have already received a message 
    """
    ignore_list = ignore_list or []
    emails_boolmap = emails_boolmap or {}
    
    required_fields = ["email", "form_path", "invoice_path", "company_name", "contact_name", "usdot"]
    
    companies_sent = set()

    for row in companies.itertuples(index=False):
        
        missing = [field for field in required_fields if not getattr(row, field, None)]
        email = getattr(row, "email", None)

        if missing:
            log.error(f"Missing {', '.join(missing)} for {email or '[no email]'}")
            continue
        
        if row.usdot in ignore_list:
            log.debug(f"Company {row.company_name} (USDOT {row.usdot} ) is in the ignore list - skipping.")
            continue

        if not emails_boolmap.get(row.email, True):
            log.debug(f"Email {row.email} is marked as invalid - skipping.")
            continue
        
        try:
            send_mcs150_and_invoice(
                email_from=email_login,
                password=email_password,
                email_to=row.email,
                mcs150_path=row.form_path,
                invoice_path=row.invoice_path,
                contact_name=row.contact_name,
                company_name=row.company_name,
                usdot=row.usdot,
                dryfire=False
            )
            pass
            companies_sent.add(row.usdot)
        except Exception as e:
            log.error(f"Error sending email to '{row.email}': {e}")
        
        if len(companies_sent) >= max_emails:
            log.debug(f"Max emails limit of {max_emails} hit at {row.email}, stopping the sending process.")
            break
        
        # Apply jitter: random delay in [delay * (1 - jitter), delay * (1 + jitter)]
        sleep_time = random.uniform(delay * (1 - jitter), delay * (1 + jitter))
        log.debug(f"Sleeping for {sleep_time:.2f} seconds before next email...")
        time.sleep(sleep_time)

    return companies_sent


def send_emails(
        email_accounts=None,
        max_emails=0,
        companies_data_file="",
        forms_dir=None,
        invoices_dir=None,
        emails_boolmap=None,
        companies_sent_file="",
        ):
    """
    Coordinates the process of sending emails with MCS-150 forms and invoices to companies.
    
    Loads company data either from a CSV or from MCS-150 forms directories, filters companies
    based on form or invoice file locations, and sends emails from a rotating set of email accounts.

    Parameters:
        email_accounts (list[str], optional): List of email login addresses to send emails from.
        max_emails (int, optional): Maximum number of emails to send per email account. Defaults to 0 (no limit).
        companies_data_file (str, optional): Path to CSV file containing company data.
        forms_dir (str, optional): Directory path containing MCS-150 forms to load companies from.
        invoices_dir (str, optional): Directory path containing invoice files to load companies from.
        emails_boolmap (dict[str, bool], optional): Mapping of email addresses to their validity status.
        companies_sent_file (str, optional): Path to file storing list of companies that have already been emailed.

    Returns:
        None

    Side effects:
        Loads and filters companies based on provided parameters.
        Sends emails to companies using provided email accounts.
        Updates and saves the list of companies already sent emails.
        Logs key events and errors during the process.
    """
    email_accounts = email_accounts or []
    emails_boolmap = emails_boolmap or {}

    log.debug(f"Creating login and password pairs by email_accounts.")
    inboxes = {}
    for login in email_accounts:
        password = Config.passwords.get(login)
        if not password:
            log.error(f"Email '{login}' app password not present in '.password.jsonc' - skipping.")
        inboxes.update({login: password})
        log.debug(f"Inbox dictionary updated successfully with {login}.")
    if not inboxes:
        log.critical(f"No usable email credentials found for email accounts.")
        return
    
    companies_sent = set(load_str_list(companies_sent_file, "companies_sent_file"))

    # Loading companies from MCS-150 forms or from a .csv
    if companies_data_file:
        log.info(f"Loading companies from csv.")
        companies_raw = pd.read_csv(companies_data_file, dtype=str)
        if forms_dir:
            log.debug(f"Filtering companies based on form_path")
            companies = companies_raw[
                companies_raw['form_path'].apply(lambda p: is_inside_dir(p, forms_dir))
            ]
        elif invoices_dir:
            log.debug(f"Filtering companies based on invoice_path")
            companies = companies_raw[
                companies_raw['invoice_path'].apply(lambda p: is_inside_dir(p, invoices_dir))
            ]
        else:
            log.debug(f"Applying no filters to companies DataFrame.")
            companies = companies_raw

    elif forms_dir and invoices_dir:
        log.info(f"Loading companies from MCS-150 forms.")
        companies = load_companies_from_forms(forms_dir, invoices_dir)
        log.info(f"Loaded {len(companies)} companies from forms.")
    else:
        missing = [name for name in ['companies_data_file', 'forms_dir', 'invoices_dir'] if locals().get(name) is None]
        log.critical(f"Cannot proceed with sending, missing arguments: {', '.join(missing)}")
        return

    # Sending emails with inbox rotation
    log.info(f"Sending emails...")
    email_count = 0
    for login, password in inboxes.items():
        log.info(f"Sending emails from inbox: '{login}'.")
        current_companies_sent = process_companies(companies, max_emails, login, password,
            ignore_list=companies_sent,
            emails_boolmap=emails_boolmap,
            delay=40
            )
        companies_sent = list(set(companies_sent).union(current_companies_sent))
        email_count += len(current_companies_sent)

    log.info(f"Total emails sent: {email_count}")

    # Updating the ignore list with processed emails
    save_str_list(
        str_list=companies_sent,
        filepath=companies_sent_file,
        label="companies_sent_file",
        mode="w"
    )

