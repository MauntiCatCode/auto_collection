from docxtpl import DocxTemplate
import pandas as pd

from context import get_company_context
from utils import batch_convert_docx_to_pdf
from log import log, MODULE_DIR


def extract_context_list(usdots: list[str], df: pd.DataFrame) -> list[dict]:
    """
    Iterates over a list of company USDOT numbers and extracts the context of those companies out of a dataframe.
    
    Args:
        usdots (list[str]): A list of USDOT numbers.
        df (pd.Dataframe): A dataframe of company details indexed by USDOT numbers.
    
    Returns:
        list[dict]: A list of context dictionaries ready to be applied via docxtpl.
    """
    context_list = []
    for usdot in usdots:
        try:
            log.debug(f"Getting company context by USDOT '{usdot}'.")
            row = df.loc[usdot]
            context = get_company_context(row)
            context_list.append(context)
        
        except KeyError:
            log.error(f"USDOT '{usdot}' not found in DataFrame.")
        except Exception as e:
            log.error(f"Error getting context for USDOT '{usdot}': {e}")

    return context_list


def fill_documents(contexts: list[dict], doc_template: str, output_dir: str) -> int:
    """
    Iterates through a list of context dictionaries and formats a chosen template with it (if present in /templates).
    Saves all the formatted documents in a given directory.

    Args:
        contexts (list[dict]): List of context dictionaries.
        doc_template (str): Template (name without extension) to be formatted (must be present in /templates).
        output_dir (str): Full path to the directory where the formatted documents will be placed.

    Returns:
        int: Number of reports saved.
    """
    saved_docs = 0

    for context in contexts:
        company_name = context.get(f"legal_name", "Unknown company")
        try:
            doc = DocxTemplate(f"templates/{doc_template}.docx")
            doc.render(context)
            
            log.debug(f"Saving rendered document at: '{output_dir}/{company_name}.docx'")

            doc.save(f"{output_dir}/{company_name}.docx")
            saved_docs += 1

        except Exception as e:
            log.error(f"Error formatting template for {company_name}: {e}")

    return saved_docs


def process_companies(usdots, df, template, output_dir) -> None:
    """
    Processes a list of USDOT numbers and company data to generate personalized reports. 
    """
    log.info(f"Creating the context list.")
    contexts = extract_context_list(usdots, df)

    log.info(f"Creating reports by template: '{MODULE_DIR}/templates/{template}'.")
    docs_count = fill_documents(contexts, template, output_dir)
    log.info(f"{docs_count} reports saved at: '{output_dir}'.")
    
    log.info(f"Converting '.docx' reports to '.pdf'.")
    batch_convert_docx_to_pdf(output_dir)
