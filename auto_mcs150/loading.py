import pandas as pd

from fetch import fetch_from_safer
from log import log


def load_companies_from_csv(path_to_csv: str, max_retries = 0, time_before_retry = 0, usdot_column = 'usdot'):
    """
    Creates a list of Company objects from a CSV by the USDOT numbers.

    Args:
    path_to_csv (str): Path to the CSV file.
    
    Returns:
    List[Company]: A list of Company objects, each created with data from SAFER based on USDOT numbers.
    """
    df = pd.read_csv(path_to_csv)
    
    if usdot_column not in df.columns:
        raise ValueError("CSV doesn't contain the usdot column specified.")
    
    companies = []

    for _, row in df.iterrows():
        usdot = row[usdot_column]
        try:
            company = fetch_from_safer(usdot, max_retries, time_before_retry)
            companies.append(company)

        except Exception as e:
            log.error(f"Company with USDOT {usdot}: {e}. Stopping the fetching of company data and returning the data already collected.")
            break
    
    return companies

