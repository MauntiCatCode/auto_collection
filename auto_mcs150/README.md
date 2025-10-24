# Auto MCS150

## Description
A tool for automation of filling out MCS-150 forms

### Background

This tool was built for use at a company offering back-office services to trucking companies and owner-operators. One of the services we offer is handling the MCS-150 form — a mandatory compliance document filed with the FMCSA.

To streamline this process and reduce manual entry, I developed `auto_mcs150` to fetch company data from the SAFER FMCSA database and automatically fill out the required PDF forms. The tool is currently used in production and integrated into our $10-per-form service offering.

## Current features
- Automatic fetching of company data from the SAFER FMCSA database, by company USDOT numbers (loaded from a .csv). (via `python_safer`)
- Filling out form fields in the MCS-150 form with the data from SAFER. (via `PyPDFForm`)
- Optional filters by date, out of service status.

## Current limitations
- The MCS-150 form still requires some human review and manual input because not all necessary data is available through the SAFER database.
- Address parsing can occasionally fail due to inconsistent or duplicate data entries on SAFER. These issues are logged to help identify and resolve problematic records.
- The tool is designed to automate as much as possible while clearly signaling when manual intervention is needed.

## Planned features
- Scraping of other databases to fill out more of the fields.
- Integration of this tool with other CLI tools of my making (`autoinvoice`, `autoemail`) into a TUI application.

## Installation
Clone this repo and install dependencies via:
`pip install -r requirements.txt`

## Usage

Navigate to the script directory and run the "auto_mcs150" file to process USDOT numbers and fill out MCS-150 forms:

`./auto_mcs150 <usdots_path> [--output_dir OUTPUT_DIR] [--path_to_mcs150_template TEMPLATE_PATH] [--before DATE] [--accept_out_of_service] [--max_retries N] [--time_before_retry SECONDS]`

- `<usdots_path>`: Path to a CSV file containing USDOT number
    *(Required)*
- `--output_dir`: Directory where filled forms will be saved. 
    *(Optional, if configured in `config.py`)*
- `--path_to_mcs150_template`: Path to the MCS-150 PDF form template.
    *(Optional, if configured in `config.py`)*
- `--before`: Include only companies that updated their MCS-150 before this date. 
    *(Optional)*
- `--accept_out_of_service`: Include companies marked as out of service.
    *(flag, default is False)*
- `--max_retries`: Number of retries on SSL errors.
    *(default: 0)*
- `--time_before_retry`: Seconds to wait before retrying.
    *(default: 0)*

### Windows users

Run the script using Python explicitly:

`python auto_mcs150 <usdots_path> [options]`
