# Modder & Translator Guide: Oracle of Ages (Koine Greek)

This guide documents the technical format, text formatting rules, control codes, and tools for modifying or extending the Koine Greek translation of *The Legend of Zelda: Oracle of Ages*.

---

## 1. Project Files

* **`text/text.yaml`**: The master dialogue script. Every dialogue entry is indexed by group and entry name (e.g. `TX_0000`, `TX_0101`).
* **`text/dict.yaml`**: The Greek compression dictionary (1,024 entries). Pre-trained on common morphemes and prefixes to compress text within Game Boy ROM banks.
* **`text/greek_map.json`**: Unicode character to tile ID mapping table. Maps polytonic Greek characters to font tiles.
* **`gfx/gfx_font.png`**: The 8×8 1-bpp/2-bpp bitmap font tilemap loaded into VRAM.
* **`patches/`**: Pre-built `.bps` and `.ips` patches ready for distribution.
* **`tools/`**: Build, compression, validation, and patch generation tools.

---

## 2. Text Box Limits & Line Widths

The Game Boy Color text box displays **16 characters (cells) per line**, and **2 lines per page**.

```
+----------------+
|1234567890123456|  <-- Line 1 (max 16 cells)
|1234567890123456|  <-- Line 2 (max 16 cells)
+----------------+
```

### Cell Width Table for Control Codes
When calculating line width, control codes have specific visual widths:

| Code | Visual Width | Description |
|---|---|---|
| Regular letters, spaces, punctuation | **1 cell** | Every Greek letter, space, period, comma, colon |
| `\Link` | **5 cells** | Replaced in-game by the player's name (up to 5 chars) |
| `\Child` | **5 cells** | Bipsen's child's name |
| `\secret1`, `\secret2` | **5 cells** | Linked game password placeholders |
| `\num1`, `\num2` | **2 cells** | Numbers / counters |
| `\heartpiece` | **2 cells** | Heart piece icon |
| `\abtn`, `\bbtn` | **2 cells** | [A] and [B] button glyphs |
| `\item(x)`, `\sym(x)` | **1 cell** | Item / symbol icon |
| `\opt()` | **1 cell** | Arrow cursor space for dialogue choice |
| `\col(x)` | **0 cells** | Color formatting command (does not advance cursor) |
| `\stop` | **0 cells** | Textbox page boundary (waits for player input) |
| `\wait`, `\slow`, `\sfx(x)` | **0 cells** | Audio / timing commands |

---

## 3. Supported Control Codes

* **Colors:**
  * `\col(0)`: Default (black text).
  * `\col(1)`: Red (items, key terms, dungeon clues).
  * `\col(2)`: Blue.
  * `\col(3)`: Green / Orange.
* **Pagination:**
  * `\stop`: Pauses printing and shows the blinking down-arrow. When the player presses [A], the textbox clears and prints the next page.
* **Choices / Options:**
  * `\opt()`: Placed at the start of selectable lines in dialogue trees.
* **Audio & Timing:**
  * `\sfx(0xNN)`: Plays a sound effect when this point in dialogue is reached.
  * `\wait`: Short pause before printing continues.

---

## 4. Polytonic Greek Orthography & Characters

The custom font (`gfx/gfx_font.png`) supports the full set of polytonic Greek characters required for Biblical / Septuagint / New Testament register:

* **Vowels with Accents:**
  * Acute (*oxia*): ά, έ, ή, ί, ό, ύ, ώ
  * Grave (*varia*): folded to acute automatically by `parseText.py` (`fold_grave: true`)
  * Circumflex (*perispomene*): ᾶ, ῆ, ῖ, ῦ, ῶ
* **Breathings:**
  * Smooth breathing (*psile*): ἀ, ἐ, ἠ, ἰ, ὀ, ὐ, ὠ
  * Rough breathing (*daseia*): ἁ, ἑ, ἡ, ἱ, ὁ, ὑ, ὡ
  * Combinations with accents: ἄ, ἅ, ἔ, ἕ, ἤ, ἥ, ἴ, ἵ, ὄ, ὅ, ὔ, ὕ, ὤ, ὥ, ἆ, ἇ, ἦ, ἧ, ἶ, ἷ, ὖ, ὗ, ὦ, ὧ
* **Iota Subscripts:**
  * ᾳ, ῃ, ῳ, ᾷ, ῇ, ῷ, ᾴ, ῄ, ῴ
* **Punctuation:**
  * Greek question mark (semicolon `;`): `U+003B`
  * Ano teleia (middle dot `·`): `U+00B7`
  * Standard punctuation: `,`, `.`, `!`, `?`, `-`, `'`

See [`docs/allowed_characters.txt`](file:///c:/Users/User/Documents/Oracle%20of%20Ages/docs/allowed_characters.txt) for the full character list.

---

## 5. Modifying & Testing the Translation

### Step 1: Edit `text/text.yaml`
Open `text/text.yaml` in any UTF-8 text editor (VS Code, Notepad++, etc.) and edit your entries. Ensure all lines stay within 16 cells.

### Step 2: Validate & Test
Run the automated build tool from the repository root:

```bash
python3 tools/build_translation.py
```

This will automatically:
1. Scan every line in `text/text.yaml` to ensure no lines exceed 16 cells and no invalid characters exist.
2. Compile and compress the script using `tools/parseText.py`.
3. Report the compressed size and verify bank fitting.

### Step 3 (Optional): Rebuild the Compression Dictionary
If you added extensive new vocabulary or dialogue, regenerate the 1,024-entry dictionary:

```bash
python3 tools/build_translation.py --rebuild-dict
```

### Step 4: Generate New ROM & Patches
To compile your changes into a `.gbc` ROM using the disassembly:
```bash
# In your oracles-disasm clone:
cp /path/to/text/text.yaml text/ages/text.yaml
cp /path/to/text/dict.yaml text/ages/dict.yaml
make ages
```

To generate updated `.bps` and `.ips` patches from your newly built `ages.gbc`:
```bash
python3 tools/create_patch.py /path/to/clean_vanilla.gbc ages.gbc patches/zelda_oracle_of_ages_greek
```
