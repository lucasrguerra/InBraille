"""Text -> Braille encoding strategies (one function per alphabet)."""
import re
from pypinyin import pinyin, Style

from src.domain.alphabets import BRAZILIAN, NORTH_AMERICAN
from src.domain import chinese_braille as cb


def encode_north_american(text):
    braille = ""
    phrases = text.split("\n")
    for phrase in phrases:
        words = phrase.replace('"', "'").split(" ")
        for word in words:
            for letter in word:
                try:
                    index_of_letter = NORTH_AMERICAN.normal.index(letter.lower())
                    braille += NORTH_AMERICAN.braille[index_of_letter]
                except:
                    pass
            braille += " "

        braille = braille.rstrip() + "\n"

    return braille.rstrip()



def encode_brazilian(text):
    treated_text = ""
    phrases = text.split("\n")
    for phrase in phrases:
        for word in phrase.split(" "):
            for index, letter in enumerate(word):
                last_letter_is_alpha = False
                next_letter_is_alpha = False

                if index > 0:
                    last_letter_is_alpha = word[index - 1].isalpha()

                if index < len(word) - 1:
                    next_letter_is_alpha = word[index + 1].isalpha()

                if last_letter_is_alpha and letter == "(":
                    treated_text += " "

                treated_text += letter
                
                if next_letter_is_alpha and letter == ")":
                    treated_text += " "

            treated_text += " "

        treated_text = treated_text.rstrip() + "\n"

    braille = ""
    phrases = treated_text.split("\n")
    for phrase in phrases:
        for word in phrase.split(" "):
            try:
                is_number = word[0].isnumeric()
                if is_number:
                    braille += "⠼"

                is_upper_case = word.isupper()
                if not is_number and is_upper_case:
                    braille += "⠨⠨"

                last_letter = None
                for letter in word:
                    index_of_letter = BRAZILIAN.normal.index(letter.lower())

                    if not is_number and letter.isnumeric():
                        braille += "⠼"
                    
                    if letter.isupper() and not is_upper_case:
                        braille += "⠨"

                    if last_letter:
                        if last_letter.isnumeric() and letter.isalpha():
                            braille += "⠂"

                    braille += BRAZILIAN.braille[index_of_letter]
                    last_letter = letter
                braille += " "
            except:
                pass

        braille = braille.rstrip() + "\n"

    return braille.rstrip().replace(" ", "⠀")


# --- Chinese (Mandarin) Encoding ---

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


def encode_chinese(text: str) -> str:
    if _contains_hanzi(text):
        text = _hanzi_to_pinyin(text)
    lines = text.split("\n")
    return "\n".join(_encode_line(line) for line in lines)