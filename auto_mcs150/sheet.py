import pandas as pd

from log import log

def append_sheet_to_fields_map(
    spreadsheet: pd.DataFrame,
    fields_map: dict[str, str],
    usdot: str,
    contact_columns: tuple[str, ...] = ("Contact Name",),
    usdot_columns: tuple[str, ...] = ("DOT#", "usdot"),
    email_columns: tuple[str, ...] = ("email", "Email")
) -> bool:
    """
    Updates fields_map with contact info from spreadsheet based on the USDOT number.

    Args:
        spreadsheet: The input DataFrame containing company data.
        fields_map: The dictionary to update with extracted fields.
        usdot: The USDOT number to match in the spreadsheet.
        contact_columns: Column names to look for contact names.
        usdot_columns: Column names to search for the USDOT number.
        email_columns: Column names to look for email addresses.

    Returns:
        True if a match was found and fields_map was updated, False otherwise.
    """
    present_contact_columns = [col for col in contact_columns if col in spreadsheet.columns]
    present_usdot_columns = [col for col in usdot_columns if col in spreadsheet.columns]
    present_email_columns = [col for col in email_columns if col in spreadsheet.columns]

    if not present_usdot_columns:
        log.error("No usable USDOT columns found in spreadsheet.")
        return False
    if not present_email_columns:
        log.error("No usable email columns found in spreadsheet.")
    if not present_contact_columns:
        log.error("No usable contact name columns found in spreadsheet.")

    usdot_norm = usdot.strip().lower()

    for _, row in spreadsheet.iterrows():
        row_usdots = [str(row[col]).strip().lower() for col in present_usdot_columns]
        if usdot_norm not in row_usdots:
            continue

        contact_str = str(row[present_contact_columns[0]]).strip() if present_contact_columns else ""
        contacts = [name.strip() for name in contact_str.split(",") if name.strip()]
        email = str(row[present_email_columns[0]]).strip() if present_email_columns else ""

        fields_map.update({
            "20eMail": email,
            "officerName1": contacts[0] if len(contacts) > 0 else "",
            "officerName2": contacts[1] if len(contacts) > 1 else "",
            "certifyName": contacts[0] if len(contacts) > 0 else "",
        })
        return True

    return False  # No match found

