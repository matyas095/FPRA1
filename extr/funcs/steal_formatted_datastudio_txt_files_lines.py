import sys
import os
import re
import numpy as np
import pandas as pd


# TO RUN: python3 steal_formatted_datastudio_txt_files_lines.py $PATH_TO_TXT

def process_txt_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 3:
        print("Error: File format is too short or invalid.")
        sys.exit(1)

    name_liner = lines[0].strip()
    header_line = lines[1].strip()

    headers = re.split(r'\s{2,}|\t+', header_line)
    if len(headers) < 2:
        headers = [h.strip() for h in header_line.split('\t') if h.strip()]

    col1_name = headers[0] if len(headers) > 0 else "-"
    col2_name = headers[1] if len(headers) > 1 else "-"

    data_rows = []
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue
        parts = re.split(r'\s{2,}|\t+', line)
        if len(parts) >= 2:
            data_rows.append(parts[:2])

    if not data_rows:
        print("Error: No valid data rows found.")
        sys.exit(1)

    df = pd.DataFrame(data_rows, columns=[col1_name, col2_name])
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    base_name = os.path.splitext(os.path.basename(filepath))[0]

    c1_clean = re.sub(r'[\s\(\)\#\/\,\.]+', '_', col1_name).strip('_')
    c2_clean = re.sub(r'[\s\(\)\#\/\,\.]+', '_', col2_name).strip('_')

    np.save(f"{base_name}_{c1_clean}.npy", df[col1_name].to_numpy())
    np.save(f"{base_name}_{c2_clean}.npy", df[col2_name].to_numpy())
    print(f"Saved NumPy files: {base_name}_{c1_clean}.npy and {base_name}_{c2_clean}.npy")

    excel_path = f"{base_name}.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Exported successfully to Excel: {excel_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_data.py <path_to_txt_file>")
        sys.exit(1)
    process_txt_file(sys.argv[1])