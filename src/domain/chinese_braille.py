"""Mainland Chinese (Mandarin) Braille tables.

Source: Australian Braille Authority, "Chinese (Mandarin) and UEB" (May 2024),
based on the official Chinese braille transcription system. Data only — the
encoding/decoding logic lives in src/translation/encoder.py and src/translation/decoder.py.

A Mandarin syllable is written with up to three cells: initial + final + tone.
Dot patterns below use dot numbers 1-6; _cell() turns them into Unicode braille.
"""


def _cell(dots: str) -> str:
    value = 0
    for dot in dots:
        value |= 1 << (int(dot) - 1)
    return chr(0x2800 + value)


BLANK = _cell("")  # empty cell, used as the space between words


# 1. Initials / consonants (dot patterns). g/j, k/q and h/x deliberately share a
# cell — the ambiguity is resolved by the following final.
_INITIAL_DOTS = {
    "b": "12", "p": "1234", "m": "134", "f": "124",
    "d": "145", "t": "2345", "n": "1345", "l": "123",
    "g": "1245", "j": "1245", "k": "13", "q": "13", "h": "125", "x": "125",
    "zh": "34", "ch": "12345", "sh": "156", "r": "245",
    "z": "1356", "c": "14", "s": "234",
}

# 2. Finals / vowels (dot patterns). Both the standalone spelling (with y/w) and the
# post-consonant spelling map to the same cell.
_FINAL_DOTS = {
    "a": "35",
    "o": "26", "e": "26",
    "i": "24", "yi": "24",
    "u": "136", "wu": "136",
    "ü": "346", "yu": "346", "v": "346",
    "er": "1235",
    "ai": "246", "ao": "235", "ei": "2346", "ou": "12356",
    "ia": "1246", "ya": "1246",
    "iao": "345", "yao": "345",
    "ie": "15", "ye": "15",
    "iu": "1256", "you": "1256",
    "ua": "123456", "wa": "123456",
    "uai": "13456", "wai": "13456",
    "ui": "2456", "wei": "2456",
    "uo": "135", "wo": "135",
    "üe": "23456", "yue": "23456", "ve": "23456",
    "an": "1236", "ang": "236", "en": "356", "eng": "3456",
    "ian": "146", "yan": "146",
    "iang": "1346", "yang": "1346",
    "in": "126", "yin": "126",
    "ing": "16", "ying": "16",
    "uan": "12456", "wan": "12456",
    "uang": "2356", "wang": "2356",
    "un": "25", "wen": "25",
    "ong": "256", "weng": "256",
    "üan": "12346", "yuan": "12346", "van": "12346",
    "ün": "456", "yun": "456", "vn": "456",
    "iong": "1456", "yong": "1456",
}

# 3. Tones, written after the syllable. Neutral tone (5/0) has no cell.
_TONE_DOTS = {"1": "1", "2": "2", "3": "3", "4": "23"}

# 5. Punctuation, in dot-pattern cells (some are multi-cell).
_PUNCTUATION_DOTS = {
    ",": ["5"],
    "，": ["5"],
    "、": ["4"],
    ";": ["56"],
    "；": ["56"],
    ":": ["36"],
    "：": ["36"],
    ".": ["5", "23"],
    "。": ["5", "23"],
    "?": ["5", "3"],
    "？": ["5", "3"],
    "!": ["56", "2"],
    "！": ["56", "2"],
    "-": ["36"],
    "…": ["5", "5", "5"],
}

# Initials whose "-i" final is not written (the buzzing/retroflex -i).
BUZZING_INITIALS = ("zh", "ch", "sh", "r", "z", "c", "s")

# Initials after which a written "u..." final is actually the "ü..." series.
YU_INITIALS = ("j", "q", "x")

# Accented pinyin vowel -> (base vowel, tone number).
ACCENTS = {
    "ā": ("a", "1"), "á": ("a", "2"), "ǎ": ("a", "3"), "à": ("a", "4"),
    "ō": ("o", "1"), "ó": ("o", "2"), "ǒ": ("o", "3"), "ò": ("o", "4"),
    "ē": ("e", "1"), "é": ("e", "2"), "ě": ("e", "3"), "è": ("e", "4"),
    "ī": ("i", "1"), "í": ("i", "2"), "ǐ": ("i", "3"), "ì": ("i", "4"),
    "ū": ("u", "1"), "ú": ("u", "2"), "ǔ": ("u", "3"), "ù": ("u", "4"),
    "ǖ": ("ü", "1"), "ǘ": ("ü", "2"), "ǚ": ("ü", "3"), "ǜ": ("ü", "4"),
    "ü": ("ü", ""),
}


# Pre-computed Unicode-braille lookups used by the encoder.
INITIAL_CELLS = {name: _cell(dots) for name, dots in _INITIAL_DOTS.items()}
FINAL_CELLS = {name: _cell(dots) for name, dots in _FINAL_DOTS.items()}
TONE_CELLS = {tone: _cell(dots) for tone, dots in _TONE_DOTS.items()}
PUNCTUATION_CELLS = {
    char: "".join(_cell(dots) for dots in cells)
    for char, cells in _PUNCTUATION_DOTS.items()
}


def _first(mapping):
    """Reverse a spelling->cell map to cell->spelling, keeping the first spelling."""
    reverse = {}
    for spelling, cell in mapping.items():
        reverse.setdefault(cell, spelling)
    return reverse


# Reverse lookups used by the decoder (cell -> canonical spelling).
INITIAL_BY_CELL = _first(INITIAL_CELLS)
FINAL_BY_CELL = _first(FINAL_CELLS)

# When a final has no preceding initial it is spelled with its y/w standalone form.
FINAL_STANDALONE_BY_CELL = {}
for _spelling, _cell_char in FINAL_CELLS.items():
    if _spelling[0] in "yw":
        FINAL_STANDALONE_BY_CELL.setdefault(_cell_char, _spelling)
for _cell_char, _plain in FINAL_BY_CELL.items():
    FINAL_STANDALONE_BY_CELL.setdefault(_cell_char, _plain)

TONE_BY_CELL = {cell: tone for tone, cell in TONE_CELLS.items()}
PUNCTUATION_BY_CELL = {
    "".join(_cell(dots) for dots in cells): char
    for char, cells in _PUNCTUATION_DOTS.items()
}
