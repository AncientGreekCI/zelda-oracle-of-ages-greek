# The Legend of Zelda: Oracle of Ages — Koine Greek Translation
### Ὁ Θρῦλος τῆς Ζέλδας: Τὸ Χρηστήριον τῶν Αἰώνων (Ἑλληνικὴ Μετάφρασις)

A complete, unabridged translation of *The Legend of Zelda: Oracle of Ages* (Game Boy Color) into **Biblical / Koine Greek** (Septuagint & New Testament register), featuring full polytonic orthography, custom 8×8 font, and full modding/rebuild tools.

---

## 🎮 How to Play (Applying the Patch)

Apply either the `.bps` (recommended) or `.ips` patch to a clean copy of the original English ROM.

### Option 1: Web Patcher (No install needed)
1. Open **[Marc Robledo's Online ROM Patcher](https://www.marcrobledo.com/RomPatcher.js/)**.
2. Under **ROM file**, choose your clean vanilla ROM: `Legend of Zelda, The - Oracle of Ages (USA, Australia).gbc`.
3. Under **Patch file**, choose `patches/zelda_oracle_of_ages_greek.bps` (or `.ips`).
4. Click **Apply patch** and save your patched `.gbc` file.

### Option 2: Desktop Patching Tools
* **Windows:** Use **[Flips (Floating IPS)](https://www.romhacking.net/utilities/1040/)** or **Lunar IPS**.
* **macOS / Linux:** Use **MultiPatch** or `flips`.

### Base ROM Specifications
Ensure your clean vanilla ROM matches these checksums:
* **ROM Title:** `Legend of Zelda, The - Oracle of Ages (USA, Australia).gbc`
* **Original Size:** 1,048,576 bytes (1.0 MB)
* **CRC32:** `3800A387`
* **MD5:** `c4639cc61c049e5a085526bb6cac03bb`
* **SHA-1:** `8ad1a3014c278bb3f0f7f32924976ea69b2d8612`

*Patched ROM Output:* 2,097,152 bytes (2.0 MB), CRC32: `F81EDF9C`.

---

## ✍️ Modifying & Rebuilding the Translation

Everything required to edit, validate, recompress, and rebuild the translation is included in this repository.

1. **Edit Dialogue:**
   Modify `text/text.yaml` in any UTF-8 text editor.
2. **Validate & Test:**
   Run the all-in-one build verification script:
   ```bash
   python3 tools/build_translation.py
   ```
   This automatically verifies line widths (max 16 cells), tests characters against `text/greek_map.json`, and verifies compression fitting.
3. **Rebuild Compression Dictionary (Optional):**
   If you add substantial new dialogue:
   ```bash
   python3 tools/build_translation.py --rebuild-dict
   ```

For detailed control codes, line-width rules, and character set reference, see the **[Modder & Translator Guide](docs/translation_guide.md)** and **[Glossary](docs/oracle_of_ages_glossary.md)**.

---

## 🛠️ Technical Details & ROM Architecture

* **Custom 8×8 Bitmap Font:** Custom font (`gfx/gfx_font.png`) mapping Greek vowels, diphthongs with breathings, and diacritics directly into the Game Boy's tile system via `text/greek_map.json`.
* **1,024-Entry Greek Compression Dictionary:** Custom compression dictionary (`text/dict.yaml`) leveraging common Greek morphemes and Game Boy control codes (`\col`, `\opt`, `\stop`, line-breaks), reducing text payload from 153 KB raw to 109 KB compressed.
* **2 MB MBC5 Bank Expansion:** Expanded ROM size from 1 MB (64 banks) to 2 MB (128 banks) and relocated the audio engine to banks `$40`–`$45`, providing limitless headroom for expanded room and graphics data.

---

## 📁 Repository Structure

```
.
├── patches/
│   ├── zelda_oracle_of_ages_greek.bps    # BPS patch (recommended)
│   └── zelda_oracle_of_ages_greek.ips    # IPS patch (legacy)
├── text/
│   ├── text.yaml                         # Master translated Greek script (2,824 entries)
│   ├── dict.yaml                         # 1,024-entry Greek compression dictionary
│   └── greek_map.json                    # Character-to-tile mapping table
├── gfx/
│   └── gfx_font.png                      # 8x8 Greek tile font
├── docs/
│   ├── translation_guide.md              # Formatting rules, control codes & modding guide
│   ├── oracle_of_ages_glossary.md        # Comprehensive translation glossary & grammar rules
│   └── allowed_characters.txt            # List of all supported polytonic Greek characters
├── tools/
│   ├── build_translation.py              # Automated validation & compilation pipeline
│   ├── validate_text.py                  # Line-width (16 cells) & character validator
│   ├── build_dict.py                     # Compression dictionary trainer / builder
│   ├── parseText.py                      # Text compiler for WLA-DX assembly
│   ├── create_patch.py                   # Standalone BPS & IPS patch generator
│   └── common.py                         # Disassembly build helper module
├── oracles_disasm_greek.patch            # Unified patch for oracles-disasm
└── README.md
```

---

## 🏗️ Building From Source

To compile the ROM from source using the [Stewmath oracles-disasm](https://github.com/Stewmath/oracles-disasm) disassembly:

1. Clone `oracles-disasm` (requires MSYS2 UCRT64 and WLA-DX v10.6):
   ```bash
   git clone https://github.com/Stewmath/oracles-disasm.git
   cd oracles-disasm
   ```
2. Apply the unified patch:
   ```bash
   git apply /path/to/oracles_disasm_greek.patch
   ```
3. Copy the translation files:
   ```bash
   cp /path/to/text/text.yaml text/ages/text.yaml
   cp /path/to/text/dict.yaml text/ages/dict.yaml
   cp /path/to/text/greek_map.json text/greek_map.json
   cp /path/to/gfx/gfx_font.png gfx/common/gfx_font.png
   ```
4. Build:
   ```bash
   make ages
   ```
   Output: `ages.gbc` (2.0 MB).

---

## ⚖️ Disclaimer

This translation patch is an unofficial fan project and is distributed under fair use for educational and linguistic preservation purposes. No copyrighted ROM binaries or proprietary Nintendo assets are included in this repository. You must supply your own legally acquired copy of *The Legend of Zelda: Oracle of Ages*.
