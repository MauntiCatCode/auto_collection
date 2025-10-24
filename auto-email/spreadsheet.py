import pandas as pd
from PyPDFForm import PdfWrapper

from utils import load_paths_from_dir, normalize_name

from config import Config
from log import log

def normalize_headers(spreadsheet, header_map : dict | None = None) -> pd.DataFrame:
    header_map = header_map or {}
    spreadsheet.columns = [header_map.get(str(col), str(col)) for col in spreadsheet.columns]
    return spreadsheet


def attach_form_paths(companies: pd.DataFrame, forms_dir, invoices_dir) -> pd.DataFrame:
    # Load paths from both directories
    forms = load_paths_from_dir(forms_dir, '.pdf')
    invoices = load_paths_from_dir(invoices_dir, '.pdf')

    # Create a lookup for invoices based on normalized names
    invoice_lookup = {normalize_name(inv): inv for inv in invoices}

    # Initialize columns for form and invoice paths
    company_form = ""
    company_invoice = ""

    # Iterate through companies to attach forms and invoices
    for idx, company in companies.iterrows():
        if not company['mcs150_last_update']:
            continue
        company_form = ""  # Reset form for each company
        company_invoice = ""  # Reset invoice for each company
        usdot = int(company['usdot']) 
        # Iterate through forms to find the matching form
        for form_path in forms:
            form = PdfWrapper(form_path).data  # Extract form data
            if str(usdot) != form.get("16usdotNumber"):
                print(f"Form USDOT: {form.get("16usdotNumber")}")
                print(f"Sheet USDOT: {usdot}")
                continue
            company_form = form_path
            break  # Break after finding the first match
        
        # If no form was found, raise an error
        if not company_form:
            log.error(f"Forms not found for USDOT {usdot}")
            continue

        # Normalize company form name to use as key for invoice lookup
        company_key = normalize_name(company_form)

        # Look up the corresponding invoice path
        company_invoice = invoice_lookup.get(company_key)

        if not company_invoice:
            log.error(f"Invoice not found for USDOT {usdot}")
            continue

        # Add the form and invoice paths to the company row
        companies.loc[idx, 'form_path'] = company_form
        companies.loc[idx, 'invoice_path'] = company_invoice
        
    return companies
        
print(Config.spreadsheet)
companies = normalize_headers(pd.read_csv(Config.spreadsheet), Config.sheet_to_df_map)

print(companies.columns)

print(attach_form_paths(companies, Config.mcs150_dir, Config.invoices_dir))