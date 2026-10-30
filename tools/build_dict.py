#!/usr/bin/env python3
"""
Build a Greek compression dictionary from the translated text, in the format parseText.py reads.

  python3 tools/build_greek_dict.py --yaml text/ages/text.yaml --out text/ages/dict_greek.yaml [--entries 250]

Method: collect every substring (3-16 characters) that occurs at least 3 times in the translated lines,
score each by the bytes it would save (occurrences x (length - 2) minus the cost of storing it), then
pick a non-overlapping set greedily, removing each chosen string from the text before choosing the next.
Control codes (\\col, \\stop, \\Link...) are excluded, so they are never inside a dictionary entry.
Dictionary entries are stored in groups 0-3 (256 slots each), as parseText.py expects.
Note: the dictionary is only used when parseText.py is run with the same entries; rebuild it after
every batch merge, then rebuild the game.
"""
import argparse, collections, re, sys, unicodedata, yaml


def fold(t):
    t = unicodedata.normalize('NFC', t)
    return unicodedata.normalize('NFC', unicodedata.normalize('NFD', t).replace('\u0300', '\u0301'))


def translated_lines(yaml_path, orig_path):
    """Only the entries that differ from the English original (i.e. the Greek ones)."""
    new = yaml.safe_load(open(yaml_path, encoding='utf-8'))
    orig = yaml.safe_load(open(orig_path, encoding='utf-8')) if orig_path else None
    out = []
    for gi, g in enumerate(new['groups']):
        for ei, e in enumerate(g['data']):
            if orig is not None:
                oe = orig['groups'][gi]['data'][ei]
                if oe['text'] == e['text']:
                    continue
            elif not re.search(r'[\u0370-\u03ff\u1f00-\u1fff]', e['text']):
                continue  # untranslated (English) entry
            for ln in fold(e['text']).split('\n'):
                for part in re.split(r'\\[A-Za-z0-9]+(?:\([^)]*\))?', ln):
                    if len(part) >= 3:
                        out.append(part)
    return out


def pick(lines, want):
    picks = []
    while len(picks) < want:
        c = collections.Counter()
        for ln in lines:
            for i in range(len(ln)):
                for n in range(3, 17):
                    if i + n <= len(ln):
                        c[ln[i:i + n]] += 1
        cand = sorted(((f * (len(s) - 2) - (len(s) + 2), s) for s, f in c.items() if f >= 3), reverse=True)
        cand = [(sc, s) for sc, s in cand if sc > 0]
        if not cand:
            break
        chosen = []
        for sc, s in cand:
            if len(chosen) >= 24 or len(picks) + len(chosen) >= want:
                break
            if any(s in x or x in s for x in chosen):
                continue
            chosen.append(s)
        if not chosen:
            break
        picks += chosen
        for s in chosen:
            lines = [p for ln in lines for p in ln.replace(s, '\x00').split('\x00') if len(p) >= 3]
    return picks[:want]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--yaml', required=True, help='current text.yaml (with Greek)')
    ap.add_argument('--orig', help='English original text.yaml (optional; restricts the input to Greek entries)')
    ap.add_argument('--out', required=True)
    ap.add_argument('--entries', type=int, default=250, help='max dictionary entries (1024 fit in 4 groups)')
    a = ap.parse_args()
    picks = pick(translated_lines(a.yaml, a.orig), a.entries)
    groups = []
    for g in range(4):
        data = [{'name': 'DICT%d_%02x' % (g, i), 'index': i, 'text': s}
                for i, s in enumerate(picks[g * 256:(g + 1) * 256])]
        if data:
            groups.append({'group': g, 'data': data})
    with open(a.out, 'w', encoding='utf-8') as f:
        yaml.safe_dump({'groups': groups}, f, allow_unicode=True, sort_keys=False)
    cost = sum(len(s.encode('utf-8')) for s in picks)
    print('wrote %d entries to %s (approx. %d bytes of dictionary text in the source)' % (len(picks), a.out, cost))


if __name__ == '__main__':
    main()
