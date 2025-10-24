import json5
import os


MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
#===User config defaults===
    SPREADSHEET_PATH = f"{MODULE_DIR}/data/companies.csv"
    OUTPUT_FORM_DIR = "/home/meow/work/MCS-150 forms"
    
#===Machine config===
    MCS150_TEMPLATE_PATH = f"{MODULE_DIR}/MCS-150 Form.pdf"

    @staticmethod
    def load_json(filename):
        with open(os.path.join(MODULE_DIR, filename), 'r') as f:
            return json5.load(f)
    
    FIELDS_MAP_TEXT = load_json('fields_map_text.jsonc')
    FIELDS_MAP_BOXES = load_json('fields_map_boxes.jsonc')
    FIELDS_MAP_ADDRESSES = load_json('fields_map_addresses.jsonc')
