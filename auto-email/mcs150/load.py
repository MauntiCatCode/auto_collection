from PyPDFForm import PdfWrapper
import pandas as pd

import os

from utils import normalize_name, load_paths_from_dir
from log import log

def extract_company_from_mcs(form_path) -> dict:
    try:
        company = {"email":None, "contact_name":None, "usdot":None}
        form_fields = PdfWrapper(str(form_path)).data
        
        company["email"] = form_fields.get("20eMail","")
        company["contact_name"] = form_fields.get("certifyName")
        company["usdot"] = form_fields.get("16usdotNumber", "")

    except Exception as e:
        log.error(f"Error reading PDF form: '{os.path.basename(form_path)}': {e}")
        return {}

    return company


def load_companies_from_forms(forms_dir, invoices_dir) -> pd.DataFrame:
    forms = load_paths_from_dir(forms_dir, '.pdf')
    invoices = load_paths_from_dir(invoices_dir, '.pdf')
    
    # Build invoice lookup by normalized company name
    invoice_lookup = {normalize_name(inv): inv for inv in invoices}
    
    data = []
    for form in forms:
        try:
            company_key = normalize_name(form)
            invoice_path = invoice_lookup.get(company_key)
            log.debug(f"Extracting data from MCS-150 form at '{form}': ")
            company = extract_company_from_mcs(form)

            company_name = company_key.upper().replace('_',' ')
            contact_name = company.get(f"contact_name", "")
            contact_name = " ".join(word.capitalize() for word in contact_name.split())
            email = company.get("email", "")
            usdot = company.get("usdot", "")

            data.append({
                "company_name" : company_name,
                "contact_name" : contact_name,
                "email": email,
                "usdot" : usdot,
                "form_path": form,
                "invoice_path": invoice_path
            })
            log.debug(f"Added company data for '{company_name}' ('{email}') to DataFrame successfully.")

        except Exception as e:
            log.error(f"Error loading company '{company_key}': {e}")
    
    companies_df = pd.DataFrame(data)

    return companies_df
