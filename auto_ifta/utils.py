import usaddress

import subprocess
import os

from log import log


def convert_to_pdf(input_path, output_pdf_path):
    """Converts DOCX to PDF using LibreOffice and saves it to the specified output path."""
    try:
        result = subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf",
            "--outdir", os.path.dirname(output_pdf_path), input_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if result.stdout:
            log.debug(result.stdout)
        if result.stderr:
            log.error(result.stderr)
        log.debug(f"PDF saved as '{output_pdf_path}'")
        return True  # Conversion successful
    except subprocess.CalledProcessError as e:
        log.error(f"Error converting '{input_path}' to PDF: {e}")
        return False  # Conversion failed


def batch_convert_docx_to_pdf(folder_path):
    """Converts all DOCX files in the given folder to PDF and returns the count of successful conversions."""
    converted_count = 0
    total_files = 0

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".docx"):
            total_files += 1
            input_path = os.path.join(folder_path, filename)
            output_pdf_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".pdf")
            log.debug(f"Converting '{input_path}' to '{output_pdf_path}'...")
            success = convert_to_pdf(input_path, output_pdf_path)
            if success:
                converted_count += 1

    log.info(f"Conversion complete: {converted_count}/{total_files} '.docx' files converted.")
    return converted_count


def split_address(address: str) -> tuple[str, str, str, str]:
    """
    Splits a US address string into (street, city, state, zipcode) using usaddress.
    """
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
