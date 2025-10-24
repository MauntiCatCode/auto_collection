from safer.search import Company
from PyPDFForm import PdfWrapper
import pandas as pd

import json
from dataclasses import dataclass, field

from config import Config
from utils import split_address
from log import log

from sheet import append_sheet_to_fields_map

@dataclass
class SimpleCompany():
    """
    Representation of a Company object filtered down to only the attributes required to fill an MCS-150 form,
    with included data normalization and formatting to make it fill-ready.
    """
    legal_name: str
    dba_name: str = ""
    usdot: str = ""
    physical_address: tuple = field(default_factory=tuple)
    mailing_address: tuple = field(default_factory=tuple)
    phone: str = ""
    mc: str = ""
    mileage: str = "0"
    operations: list = field(default_factory=list)
    operation_classifications: list = field(default_factory=list)
    cargo_carried: list = field(default_factory=list)

    @classmethod
    def from_company(cls, company: Company) -> "SimpleCompany":
        physical_address, mailing_address = (), ()
        try:
            physical_address = split_address(company.physical_address)
            # Split and assign mailing address not equal to physical address
            mailing_address = split_address(company.mailing_address) if company.mailing_address != company.physical_address else ()
        except Exception as e:
            log.warning(f"Error when splitting address for '{company.legal_name}' (USDOT {company.usdot}): {e}")

        return cls(
            legal_name=company.legal_name,
            dba_name=company.dba_name or "",
            usdot=str(company.usdot),
            physical_address=physical_address,
            mailing_address=mailing_address, 
            phone=company.phone_number or "",
            mc=company.mc_mx_ff_numbers.strip('-') if company.mc_mx_ff_numbers else "",
            mileage=f"{company.mcs_150_mileage_year['mileage']:,}" if company.mcs_150_mileage_year["mileage"] else "0",
            operations=company.carrier_operation or [],
            operation_classifications=company.operation_classification or [],
            cargo_carried=company.cargo_carried or []
        )


    def map_to_form_fields(self) -> dict:
        """
        Maps SimpleCompany instance to a dictionary of MCS-150 form fields and their corresponding values.

        Uses Config mappings:
            - FIELDS_MAP_TEXT: property name to form text field
            - FIELDS_MAP_ADDRESSES: property name to tuple of form address fields
            - FIELDS_MAP_BOXES: operation codes to checkbox fields
        """
        fields = {}

        for _property, value in self.__dict__.items():
            # Handle mappings based on Config.FIELDS_MAP_TEXT
            if _property in Config.FIELDS_MAP_TEXT:
                fields[Config.FIELDS_MAP_TEXT.get(_property)] = value
                continue

            # Handle address fields using Config.FIELDS_MAP_ADDRESSES
            if _property in Config.FIELDS_MAP_ADDRESSES:
                addr_category = Config.FIELDS_MAP_ADDRESSES.get(_property)
                addr = value
                fields.update({
                    field: addr_component
                    for field, addr_component in zip(addr_category, addr)
                })
                continue

            # Handle box fields using Config.FIELDS_MAP_BOXES
            for v in value:
                if v not in Config.FIELDS_MAP_BOXES:
                    log.warning(f"{v} property of Company {self.legal_name} (USDOT: {self.usdot}) is not in any of the field maps.")
                    continue

                field = Config.FIELDS_MAP_BOXES.get(v)
                fields[field] = True

        return fields


    def filled_form(self, mcs150_template_path, spreadsheet_path) -> PdfWrapper:
        log.debug(f"Filling MCS-150 Form for company '{self.legal_name}' (USDOT: {self.usdot})'...")
        form = PdfWrapper(mcs150_template_path)
        filled_fields = self.map_to_form_fields()

        # "There is nothing more permanent than a temporary solution"
        # TEMPORARY SIDE EFFECT - GETTIND DATA FROM SPREADSHEET FOR FILLING
        log.debug(f"Adding spreadsheet info for company '{self.legal_name}' (USDOT: {self.usdot})...")
        try:
            filled_fields_copy = filled_fields.copy()
            spreadsheet = pd.read_csv(spreadsheet_path) 
            append_sheet_to_fields_map(spreadsheet, filled_fields_copy, self.usdot)
            filled_fields = filled_fields_copy
        except Exception as e:
            log.warning(f"Error appending spreadsheet info for company '{self.legal_name}' (USDOT: {self.usdot}): {e}")

        form.fill(filled_fields)
        return form


    def to_json(self):
        return json.dumps({
            "legal_name": self.legal_name,
            "dba_name": self.dba_name,
            "usdot": self.usdot,
            "physical_address": self.physical_address,
            "mailing_address": self.mailing_address,
            "phone": self.phone,
            "mc": self.mc,
            "mileage": self.mileage,
            "operations": self.operations,
            "operation_classifications": self.operation_classifications,
            "cargo_carried": self.cargo_carried
        }, default=str, indent=4)


    def __str__(self):
        # Preprocess each section
        dba_str = f"\n    DBA name: {self.dba_name}" if self.dba_name else ""
        mailing_address_str = f"\n    Mailing address:\n        {'\n        '.join(self.mailing_address)}" if self.mailing_address else ""
        mc_str = f"\n    MC: {self.mc}" if self.mc else ""
        
        operations_str = ";\n        ".join(self.operations)
        operation_classifications_str = ";\n        ".join(self.operation_classifications)
        cargo_classifications_str = ";\n        ".join(self.cargo_carried)
        physical_address_str = "\n        ".join(self.physical_address)

        # Now use the preprocessed variables in the f-string
        return f"""
Legal name: {self.legal_name}{dba_str}
Physical address:
    {physical_address_str}{mailing_address_str}
Phone: {self.phone}
USDOT: {self.usdot}{mc_str}
Mileage: {self.mileage}
Company operations:
    {operations_str} Carrier
Operation classifications:
    {operation_classifications_str}
Cargo classifications:
    {cargo_classifications_str}
        """
    
