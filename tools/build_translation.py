#!/usr/bin/env python3
"""
All-in-one build and test tool for Oracle of Ages (Koine Greek Translation).
Usage:
  python3 tools/build_translation.py [--rebuild-dict]
"""
import argparse
import os
import subprocess
import sys
import tempfile

def main():
    parser = argparse.ArgumentParser(description="Build and test the Koine Greek translation.")
    parser.add_argument("--rebuild-dict", action="store_true", help="Re-train and rebuild the compression dictionary")
    parser.add_argument("--yaml", default="text/text.yaml", help="Path to text.yaml")
    parser.add_argument("--dict", default="text/dict.yaml", help="Path to dict.yaml")
    parser.add_argument("--map", default="text/greek_map.json", help="Path to greek_map.json")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    print("==================================================")
    print(" 1. Validating Text (Line widths & Characters)... ")
    print("==================================================")
    val_ret = subprocess.call([sys.executable, "tools/validate_text.py", "--yaml", args.yaml, "--map", args.map])
    if val_ret != 0:
        print("\n[ERROR] Text validation failed! Please fix the errors listed above.")
        sys.exit(1)

    if args.rebuild_dict:
        print("\n==================================================")
        print(" 2. Rebuilding Compression Dictionary...          ")
        print("==================================================")
        dict_ret = subprocess.call([sys.executable, "tools/build_dict.py", "--yaml", args.yaml, "--out", args.dict, "--entries", "1024"])
        if dict_ret != 0:
            print("\n[ERROR] Dictionary rebuild failed!")
            sys.exit(1)

    print("\n==================================================")
    print(" 2. Compiling & Compressing Text...               ")
    print("==================================================")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_text_data = os.path.join(tmpdir, "textData.s")
        # Base address: 0x74000 (Ages)
        cmd = [
            sys.executable,
            "tools/parseText.py",
            args.dict,
            args.yaml,
            tmp_text_data,
            str(0x74000),
            "--greek-map",
            args.map
        ]
        parse_ret = subprocess.call(cmd)
        if parse_ret != 0:
            print("\n[ERROR] Text compilation / compression failed!")
            sys.exit(1)

        size = os.path.getsize(tmp_text_data)
        print(f"\nText compilation SUCCESS!")
        print(f"Generated text assembly: {size:,} bytes")
        print("Everything is verified and ready to build into ROM with 'make ages'.")

if __name__ == "__main__":
    main()
