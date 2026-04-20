#!/usr/bin/env python3

import sys
import pathlib
import subprocess

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <json-folder> <csv-folder>",file=sys.stderr)
        sys.exit(1)
    input_dir = pathlib.Path(sys.argv[1])
    output_dir = pathlib.Path(sys.argv[2])

    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' not a directory.", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    for json_file in input_dir.glob("*.json"):
        print(f"Converting {json_file.name} ...")
        output_file = output_dir / json_file.with_suffix(".csv").name
        try:
            with open(output_file,"w") as f_out:
                subprocess.run(
                    ["./json2csv-file",str(json_file)],
                    stdout=f_out,
                    check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {json_file.name}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()