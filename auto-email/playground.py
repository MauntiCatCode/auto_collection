import pandas as pd

from config import Config, MODULE_DIR
import pandas as pd

from utils import load_str_list

# --- File paths ---
input_csv_path = Config.companies_csv_path
already_contacted_txt = Config.companies_sent_file
output_csv_path = f'{MODULE_DIR}/filtered_new_targets.csv'

# --- Load CSV with all data (dtype=str) ---
df = pd.read_csv(input_csv_path, dtype=str, keep_default_na=False)

# --- Load list of already-messaged USDOTs ---
already_sent_usdots = set(load_str_list(already_contacted_txt))

# --- Filter: keep only rows where 'usdot' not in the already-sent set ---
df_filtered = df[~df['usdot'].isin(already_sent_usdots)]

# --- Save result ---
df_filtered.to_csv(output_csv_path, index=False)

print(f"Saved {len(df_filtered)} rows to {output_csv_path} (excluding {len(already_sent_usdots)} already-contacted USDOTs)")
