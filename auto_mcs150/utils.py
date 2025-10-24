from datetime import datetime as dt
import usaddress

from config import Config
from log import log


def split_address(address : str) -> tuple[str, str, str, str]:
    parsed_address = usaddress.tag(address)[0]

    street = []
    for key, value in parsed_address.items():
        if key == "PlaceName":
            break
        street.append(value) if value else street.append("")
    street = " ".join(street)

    city = parsed_address.get("PlaceName", "")
    state = parsed_address.get("StateName", "")
    zipcode = parsed_address.get("ZipCode", "")

    return (street, city, state, zipcode)


def handled_paths(args) -> dict:
    # Handle path_to_mcs150_template argument, fallback to Config.MCS150_TEMPLATE_PATH
    if not args.path_to_mcs150_template:
        if not Config.MCS150_TEMPLATE_PATH:
            raise ValueError("No path to MCS-150 template provided, and MCS150_TEMPLATE_PATH is not configured.")
        else:
            log.debug(f"Using 'MCS150_TEMPLATE_PATH' set in 'config.py': {Config.MCS150_TEMPLATE_PATH}")
            path_to_mcs150_template = Config.MCS150_TEMPLATE_PATH
    else:
        path_to_mcs150_template = args.path_to_mcs150_template
    
    # Handle path_to_mcs150 argument, fallback to MCS150_PATH
    if not args.output_dir:
        if not Config.OUTPUT_FORM_DIR:
            raise ValueError("No output directory provided, and OUTPUT_FORM_DIR is not configured.")
        else:
            log.debug(f"Using OUTPUT_FORM_DIR set in 'config.py' as output directory: '{Config.OUTPUT_FORM_DIR}'")
            path_to_mcs150 = Config.OUTPUT_FORM_DIR
    else:
        path_to_mcs150 = args.output_dir

    return {"path_to_mcs150_template": path_to_mcs150_template, "path_to_mcs150" : path_to_mcs150}


def parse_datetime(date_str):
    # European format
    return dt.strptime(date_str, '%d.%m.%Y')


