#!/usr/bin/env python3

import sys
import pathlib
import subprocess

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <csv-unprocessed-folder> <csv-processed-folder>", file=sys.stderr)
        sys.exit(1)

    input_dir = pathlib.Path(sys.argv[1])
    output_dir = pathlib.Path(sys.argv[2])
    processed_count = 0
    errors = []
    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' not a directory.", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    fails = output_dir / "failed"

    for csv_file in input_dir.glob("*.csv"):
        if not csv_file.is_file():
            continue
        if csv_file.stem.endswith("-processed"):
            continue
        print(f"Processing {csv_file.name} ...")
        output_file = output_dir / f"{csv_file.stem}-processed{csv_file.suffix}"
        try:
            with open(csv_file, 'r') as f_in, open(output_file, 'w') as f_out:
                subprocess.run(
                    [sys.executable, "process_feedback.py"],
                    stdin=f_in,
                    stdout=f_out,
                    check=True )
            processed_count += 1
        except subprocess.CalledProcessError:
            print(f"Error processing {csv_file.name}", file=sys.stderr)
            fails.mkdir(parents=True,exist_ok=True)
            errors.append(csv_file.name)
            output_file.rename(fails / output_file.name)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
    print(f"Successfully processed {processed_count} files")
    if errors:
        if len(errors) == 1:
            print("1 file failed:")
        else:
            print(f"{len(errors)} files failed:")
        for file in errors:
            print(file)
        print(f"Partial output for failed files can be found in {fails}")

if __name__ == "__main__":
    main()