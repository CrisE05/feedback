#!/usr/bin/env python3

import sys
import pathlib
import pandas as pd
import subprocess
import shutil

def convert(csv_file, xlsx_file,conv_opt):
    if conv_opt == 1:
        subprocess.run(
                ["ssconvert", str(csv_file), str(xlsx_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
    elif conv_opt == 2:
            df = pd.read_csv(csv_file)
            df.to_excel(xlsx_file, index=False, engine='openpyxl')

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} [options] <csv-folder> <xlsx-folder>", file=sys.stderr)
        print("Options are \n\
            \t-p, --pandas for conversion with pandas\n\
            \t-s, --ssconvert or nothing for conversion with ssconverct",file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) == 3 or sys.argv[1] == "-s" or sys.argv[1] == "--ssconvert":
        if shutil.which("ssconvert") is None:
            print('Error: ssconvert missing (search for the "gnumeric" package)', file=sys.stderr)
            sys.exit(1)
        conv_opt = 1
    elif sys.argv[1] == "-p" or sys.argv[1] == "---pandas":
        conv_opt = 2
    else:
        print(f"{sysy.argv[3]} is not a valid option")
        print("Options are \n\
            \t-p, --pandas for conversion with pandas\n\
            \t-s, --ssconvert or nothing for conversion with ssconverct",file=sys.stderr)
        sys.exit(1)

    input_dir = pathlib.Path(sys.argv[2])
    output_dir = pathlib.Path(sys.argv[3])
    output_dir.mkdir(parents=True, exist_ok=True)

    for csv_file in input_dir.glob("*.csv"):
        if not csv_file.is_file():
            continue

        xlsx_file = output_dir / csv_file.with_suffix('.xlsx').name
        print(f"Convert {csv_file} to {xlsx_file} format...")

        try:
            convert(csv_file,xlsx_file,conv_opt)
        except Exception as e:
            print(f"Failed to convert {csv_file.name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()