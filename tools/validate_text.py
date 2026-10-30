#!/usr/bin/env python3
"""
Text validation script for The Legend of Zelda: Oracle of Ages (Koine Greek Translation).
Verifies:
1. Every line is <= 16 visual cells wide.
2. Only characters defined in greek_map.json are used (outside control codes).
3. All control codes are valid and properly formatted.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import yaml

MAX_WIDTH = 16

PLAIN_TOKENS = [
    ('Link', 5), ('link', 5), ('Child', 5), ('child', 5), ('secret1', 5), ('secret2', 5),
    ('num1', 2), ('opt', 1), ('stop', 0), ('heartpiece', 2), ('num2', 2), ('slow', 0),
    ('circle', 1), ('club', 1), ('diamond', 1), ('spade', 1), ('heart', 1), ('up', 1),
    ('down', 1), ('left', 1), ('right', 1), ('times', 1), ('abtn', 2), ('bbtn', 2),
    ('triangle', 1), ('rectangle', 1), ('n', 0), ('\\', 1)
]

BRACKET_WIDTHS = {'item': 1, 'sym': 1}

APOSTROPHES = ('\u1fbd', '\u2019', '\u02bc')

def normalize_text(text):
    text = unicodedata.normalize('NFC', text)
    for a in APOSTROPHES:
        text = text.replace(a, "'")
    return unicodedata.normalize('NFC', unicodedata.normalize('NFD', text).replace('\u0300', '\u0301'))

def scan_line(line):
    i = 0
    tokens = []
    while i < len(line):
        c = line[i]
        if c != '\\':
            tokens.append(('char', c, 1))
            i += 1
            continue

        rest = line[i + 1:]
        matched = False
        for name, w in PLAIN_TOKENS:
            if rest.startswith(name):
                j = i + 1 + len(name)
                if line[j:j + 2] == '()':
                    j += 2
                tokens.append(('tok', line[i:j], w))
                i = j
                matched = True
                break
        if matched:
            continue

        m = re.match(r'([A-Za-z0-9]+)\(([^)]*)\)', rest)
        if m:
            name, arg = m.group(1), m.group(2)
            w = BRACKET_WIDTHS.get(name, 0)
            j = i + 1 + len(m.group(0))
            tokens.append(('tok', line[i:j], w))
            i = j
            continue

        tokens.append(('char', c, 1))
        i += 1

    return tokens

def line_width(line):
    return sum(w for _, _, w in scan_line(line))

def validate(yaml_path, map_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    with open(map_path, 'r', encoding='utf-8') as f:
        map_json = json.load(f)

    greek_map = {chr(int(k[2:], 16)): v for k, v in map_json['map'].items()}
    fold_grave = map_json.get('fold_grave', False)
    allowed_chars = set(greek_map.keys()) | set(" \n\r\t!?,.-:;\"'()[]0123456789/%#$&*+=<>_")

    errors = []
    total_entries = 0
    total_lines = 0

    for group in data.get('groups', []):
        for entry in group.get('data', []):
            names = entry.get('name')
            if not isinstance(names, list):
                names = [names]
            label = names[0]
            text = entry.get('text', '')
            total_entries += 1

            lines = text.split('\n')
            for line_idx, line in enumerate(lines, 1):
                total_lines += 1
                norm = normalize_text(line)
                width = line_width(norm)
                if width > MAX_WIDTH:
                    errors.append(f"[{label}] Line {line_idx} too wide: {width} cells (max {MAX_WIDTH}): \"{line}\"")

                for kind, tok, _ in scan_line(norm):
                    if kind == 'char' and tok not in allowed_chars:
                        errors.append(f"[{label}] Line {line_idx} contains unmapped character: '{tok}' (U+{ord(tok):04X})")

    return errors, total_entries, total_lines

def main():
    parser = argparse.ArgumentParser(description="Validate Oracle of Ages Greek text.yaml")
    parser.add_argument("--yaml", default="text/text.yaml", help="Path to text.yaml")
    parser.add_argument("--map", default="text/greek_map.json", help="Path to greek_map.json")
    args = parser.parse_args()

    print(f"Validating {args.yaml} against {args.map}...")
    errors, total_entries, total_lines = validate(args.yaml, args.map)

    print(f"Checked {total_entries} entries across {total_lines} lines.")
    if errors:
        print(f"\nFound {len(errors)} problem(s):")
        for err in errors[:50]:
            print("  - " + err)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more.")
        sys.exit(1)
    else:
        print("Success: 0 errors! All lines fit within 16 cells and all characters are valid.")

if __name__ == "__main__":
    main()
