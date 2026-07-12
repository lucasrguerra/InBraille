"""Mandarin Chinese ↔ Braille conversion.

Encoding accepts either pinyin (numbered tones like "ni3" or accented like "nǐ") or
Chinese characters (converted to pinyin with pypinyin first). A syllable is written as
initial + final + tone, following the official Chinese braille rules.

Decoding returns pinyin with numbered tones (recovering the original Chinese characters
is not possible from the phonetic braille alone).
"""
import re

from pypinyin import pinyin, Style

from src.domain import chinese_braille as cb


_HAN_RE = re.compile(r"[一-鿿]")


def _contains_hanzi(text: str) -> bool:
    return bool(_HAN_RE.search(text))


def _han_chunks(text: str):
    """Yield (is_han, chunk) runs so Han characters convert with polyphone context."""
    for is_han, group in _group_by(text, lambda c: bool(_HAN_RE.match(c))):
        yield is_han, group


def _group_by(text, key):
    if not text:
        return
    current_key = key(text[0])
    buffer = text[0]
    for char in text[1:]:
        k = key(char)
        if k == current_key:
            buffer += char
        else:
            yield current_key, buffer
            current_key, buffer = k, char
    yield current_key, buffer


def _hanzi_to_pinyin(text: str) -> str:
    parts = []
    for is_han, chunk in _han_chunks(text):
        if is_han:
            syllables = pinyin(chunk, style=Style.TONE3, neutral_tone_with_five=True)
            parts.append("".join(s[0] for s in syllables))
        else:
            parts.append(chunk)
    return "".join(parts)


# --- Encoding ---------------------------------------------------------------

def encode_chinese(text: str) -> str:
    if _contains_hanzi(text):
        text = _hanzi_to_pinyin(text)
    lines = text.split("\n")
    return "\n".join(_encode_line(line) for line in lines)


def _encode_line(line: str) -> str:
    words = line.split(" ")
    return cb.BLANK.join(_encode_word(word) for word in words)


def _encode_word(word: str) -> str:
    cells = []
    buffer = ""
    for char in word:
        if char in cb.PUNCTUATION_CELLS:
            if buffer:
                cells.append(_encode_pinyin(buffer))
                buffer = ""
            cells.append(cb.PUNCTUATION_CELLS[char])
        else:
            buffer += char
    if buffer:
        cells.append(_encode_pinyin(buffer))
    return "".join(cells)


def _strip_accents(segment: str):
    plain = []
    tones = {}
    for char in segment:
        if char in cb.ACCENTS:
            base, tone = cb.ACCENTS[char]
            if tone:
                tones[len(plain)] = tone
            plain.append(base)
        else:
            plain.append(char)
    return "".join(plain), tones


def _parse_syllables(plain: str, tones: dict):
    result = []
    index = 0
    length = len(plain)
    while index < length:
        char = plain[index]
        if char in "'’ " or char.isdigit():
            index += 1
            continue

        start = index
        initial = ""
        if plain[index:index + 2] in cb.INITIAL_CELLS:
            initial = plain[index:index + 2]
            index += 2
        elif plain[index:index + 1] in cb.INITIAL_CELLS:
            initial = plain[index]
            index += 1

        rest = plain[index:]
        if initial in cb.YU_INITIALS and rest[:1] == "u":
            rest = "ü" + rest[1:]

        final = ""
        for size in range(4, 0, -1):
            candidate = rest[:size]
            if candidate in cb.FINAL_CELLS:
                final = candidate
                index += size
                break

        tone = ""
        if index < length and plain[index] in "012345":
            tone = plain[index]
            index += 1
        if not tone:
            for position in range(start, index):
                if position in tones:
                    tone = tones[position]
                    break

        if not initial and not final:
            index = start + 1
            continue

        result.append((initial, final, tone))
    return result


def _encode_pinyin(segment: str) -> str:
    plain, tones = _strip_accents(segment)
    return "".join(_encode_syllable(*syllable) for syllable in _parse_syllables(plain, tones))


def _encode_syllable(initial: str, final: str, tone: str) -> str:
    cells = ""
    if initial in cb.BUZZING_INITIALS and final == "i":
        # The buzzing/retroflex -i is not written: only the initial.
        cells += cb.INITIAL_CELLS[initial]
    elif initial == "d" and final == "e" and tone in ("", "5", "0"):
        # Neutral "de" (的/地/得) is contracted to the initial d.
        cells += cb.INITIAL_CELLS["d"]
        tone = ""
    else:
        if initial:
            cells += cb.INITIAL_CELLS[initial]
        if final:
            cells += cb.FINAL_CELLS[final]

    if tone in cb.TONE_CELLS:
        cells += cb.TONE_CELLS[tone]
    return cells


# --- Decoding ---------------------------------------------------------------

_YU_FINALS = {"ü": "u", "üe": "ue", "üan": "uan", "ün": "un"}
_I_OR_YU_START = ("i", "ü")


def decode_chinese(braille: str) -> str:
    lines = braille.split("\n")
    return "\n".join(_decode_line(line) for line in lines)


def _decode_line(line: str) -> str:
    words = line.split(cb.BLANK)
    return " ".join(_decode_word(word) for word in words if word)


def _match_punctuation(word: str, index: int):
    # Try the longest punctuation cell sequence first (up to 3 cells).
    for size in (3, 2, 1):
        chunk = word[index:index + size]
        if chunk in cb.PUNCTUATION_BY_CELL:
            return cb.PUNCTUATION_BY_CELL[chunk], size
    return None


def _decode_word(word: str) -> str:
    output = ""
    index = 0
    length = len(word)
    while index < length:
        punctuation = _match_punctuation(word, index)
        if punctuation:
            output += punctuation[0]
            index += punctuation[1]
            continue

        cell = word[index]
        initial = cb.INITIAL_BY_CELL.get(cell)
        has_initial = initial is not None
        if has_initial:
            index += 1

        final_cell = None
        if index < length and word[index] in cb.FINAL_BY_CELL:
            final_cell = word[index]
            index += 1

        tone = ""
        if index < length and word[index] in cb.TONE_BY_CELL:
            tone = cb.TONE_BY_CELL[word[index]]
            index += 1

        if not has_initial and final_cell is None:
            index += 1  # unknown cell
            continue

        output += _render_syllable(initial or "", final_cell, tone)
    return output


def _render_syllable(initial: str, final_cell, tone: str) -> str:
    if initial and final_cell is None:
        # Contracted single-cell syllables.
        if initial in cb.BUZZING_INITIALS:
            syllable = initial + "i"
        elif initial == "d":
            syllable = "de"
        else:
            syllable = initial
        return syllable + tone

    if final_cell is None:
        return tone

    if not initial:
        final = cb.FINAL_STANDALONE_BY_CELL.get(final_cell, cb.FINAL_BY_CELL[final_cell])
        return final + tone

    final = cb.FINAL_BY_CELL[final_cell]

    # Resolve the shared initial cells using the following final.
    if final[0] in _I_OR_YU_START:
        initial = {"g": "j", "k": "q", "h": "x"}.get(initial, initial)

    # After j/q/x the ü-finals are spelled with a plain u.
    if initial in cb.YU_INITIALS and final in _YU_FINALS:
        final = _YU_FINALS[final]

    return initial + final + tone
