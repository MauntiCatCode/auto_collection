
from datetime import datetime

from utils import parse_datetime
from company import SimpleCompany
from log import log


def filter_company(
    company, 
    exclude_out_of_service: bool = True, 
    before: str | datetime | None = None
):
    """
    Filters a Company object based on:
    - Out-of-service status (if `exclude_out_of_service` is True)
    - MCS-150 last update date (if `before` is provided)

    Returns a Company object if it passes filters, otherwise None.
    """
    if not company:
        return
    
    reasons = []

    if exclude_out_of_service and company.out_of_service_date:
        reasons.append("Company is out of service")

    if before:
        if isinstance(before, str):
            before = parse_datetime(before)

        if not company.mcs_150_form_date:
            reasons.append("Missing MCS-150 last update date")
        elif company.mcs_150_form_date >= before:
            reasons.append(f"MCS-150 update is after {before}")

    if reasons:
        log.debug(
            f"Filtering out company '{company.legal_name}' (USDOT: {company.usdot}) due to: {', '.join(reasons)}"
        )
        return None

    log.debug(
        f"Company '{company.legal_name}' (USDOT: {company.usdot}) passed filters: "
        + f"{'exclude out of service' if exclude_out_of_service else ''}"
        + f"{', before ' + before.isoformat() if before else ''}"
    )

    return company


def filtered_companies(companies, exclude_out_of_service = True, before = None):
    filtered_companies = []
    
    for comp in companies:
        try:
            if not filter_company(comp, exclude_out_of_service, before):
                continue
            filtered_companies.append(SimpleCompany.from_company(comp))
        except Exception as e:
            log.error(f"Error when filtering company '{comp.legal_name or "Unknown"}': {e}")
            continue
        
    return filtered_companies