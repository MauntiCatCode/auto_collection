from safer import CompanySnapshot
from safer.exceptions import CompanySnapshotNotFoundException, SAFERUnreachableException
from safer.results import Company
from requests.exceptions import SSLError

import time

from log import log

CLIENT = CompanySnapshot()


def fetch_from_safer(usdot, max_retries = 0, time_before_retry = 0) -> Company | None:
    """
    Fetches company details based on a given USDOT number from SAFER and handles errors like
    company not found, too many requests

    Args:
    usdot: The USDOT number of the company to retrieve (required).
    max_retries: The maximum number of retry attempts in case of an SSLError (required).
    time_before_retry: The number of seconds to wait before retrying after an SSLError (required).

    Returns:
        Optional[Company]: The company object if the fetch is successful and no errors occur, or `None` if 
                            an error occurs or the company does not meet the provided criteria.

    Error Handling:
        - If the USDOT number is not found, an error is logged and `None` is returned.
        - If there is an SSLError due to too many requests to SAFER, the function will retry the request up to 
          the maximum number of retries, waiting for the specified time before each retry.
    """
    log.debug(f"Fetching data from SAFER by USDOT: {usdot}...")

    try:
        company = CLIENT.get_by_usdot_number(int(usdot))
    except CompanySnapshotNotFoundException:
        log.warning(f"Company with USDOT {usdot} not found.")
        return
    except SSLError or SAFERUnreachableException as e:
        if max_retries > 0: # Base case
            log.error(f"The SAFER website is currently unreachable. Waiting {time_before_retry} seconds before retry. Retries left: {max_retries}.")
            time.sleep(time_before_retry)
            return fetch_from_safer(usdot, max_retries-1, time_before_retry) # Retry recursively until max_retries hit 0 
        else:
            raise e

    return company

