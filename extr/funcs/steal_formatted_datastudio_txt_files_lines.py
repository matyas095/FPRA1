import sys
import os
import re
import glob
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

current_dir = Path(__file__).resolve().parent

root_dir = current_dir
while not (root_dir / "extr").exists() and root_dir != root_dir.parent:
    root_dir = root_dir.parent


def process_txt_file(filepath, output_path=None, copy_to_clipboard=False):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    if output_path and not os.path.exists(output_path):
        print(f"Error: Output path '{output_path}' not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 3:
        print(f"Error: File '{filepath}' format is too short or invalid.")
        return

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
        print(f"Error: No valid data rows found in '{filepath}'.")
        return

    df = pd.DataFrame(data_rows, columns=[col1_name, col2_name])
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    base_name = os.path.splitext(os.path.basename(filepath))[0]

    c1_clean = re.sub(r'[\s\(\)\#\/\,\.]+', '_', col1_name).strip('_')
    c2_clean = re.sub(r'[\s\(\)\#\/\,\.]+', '_', col2_name).strip('_')

    if output_path is not None:
        combined_path = Path(output_path).resolve()
    else:
        combined_path = current_dir

    np.save(f"{combined_path}/{base_name}_{c1_clean}.npy", df[col1_name].to_numpy())
    np.save(f"{combined_path}/{base_name}_{c2_clean}.npy", df[col2_name].to_numpy())
    print(f"Saved NumPy files: {base_name}_{c1_clean}.npy and {base_name}_{c2_clean}.npy - To Path: {combined_path}")

    excel_path = f"{combined_path}/{base_name}.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Exported successfully to Excel: {base_name}.xlsx - To Path: {combined_path}")

    if copy_to_clipboard:
        try:
            df_clipboard = df.copy()
            for col in df_clipboard.columns:
                df_clipboard[col] = df_clipboard[col].astype(str).str.replace('.', ',')

            df_clipboard.to_clipboard(index=False, header=False)
            print("Successfully copied DataFrame to clipboard (without headers, with comma decimals)!")
        except Exception as e:
            print(f"Warning: Could not copy to clipboard: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process formatted Data Studio text files in batch.")
    parser.add_argument("filepaths", nargs="+", type=str, help="Path(s) to the txt file(s) or pattern (e.g., *.txt)")
    parser.add_argument("-out", "--output", type=str, default=None, help="Optional output directory path")
    parser.add_argument("-ct", "--clipboard", action="store_true", help="Copy DataFrame to clipboard")

    args = parser.parse_args()

    resolved_files = []
    for pattern in args.filepaths:
        matched = glob.glob(pattern)
        if matched:
            resolved_files.extend(matched)
        else:
            resolved_files.append(pattern)

    resolved_files = list(dict.fromkeys(resolved_files))

    if not resolved_files:
        print("Error: No files matched the given path(s).")
        sys.exit(1)

    for filepath in resolved_files:
        print(f"\nProcessing: {filepath}")
        process_txt_file(filepath, args.output, args.clipboard)