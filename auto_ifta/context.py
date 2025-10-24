from utils import split_address


def get_company_context(row):
    # Get and split address
    address = split_address(row["Physical Address"])

    context = {
        # NEW SPREADSHEET SYNTAX
        "legal_name": row["Name"],
        "contact_name": row["Contact Name"],
        "phone": row["Phone"],
        "email": row["Email"],
        # Insert split address
        "street": address[0],
        "city": address[1],
        "state": address[2],
        "zip": address[3]
        }
    return context