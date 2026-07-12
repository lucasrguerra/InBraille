"""Braille -> text decoding strategies (one function per alphabet)."""
from src.domain.alphabets import BRAZILIAN, NORTH_AMERICAN
from src.domain import chinese_braille as cb


def decode_north_american(braille):
    text = ""
    phrases = braille.split("\n")
    for phrase in phrases:
        words = phrase.replace('"', "'").split(" ")
        for word in words:
            for letter in word:
                try:
                    index_of_letter = NORTH_AMERICAN.braille.index(letter)
                    text += NORTH_AMERICAN.normal[index_of_letter]
                except:
                    pass
            text += " "

        text = text.rstrip() + "\n"

    return text.rstrip()



def decode_brazilian(braille):
    text = ""
    phrases = braille.split("\n")
    for phrase in phrases:
        for word in phrase.split("⠀"):
            try:
                treated_word = word

                is_number = word[0] == "⠼"
                if is_number:
                    treated_word = treated_word[1:]

                if word.startswith("⠣⠄"):
                    text += "("
                    treated_word = treated_word[2:]

                if word.startswith("⠷⠄"):
                    text += "["
                    treated_word = treated_word[2:]

                if word.endswith("⠄⠜"):
                    treated_word = treated_word[:-2]

                if word.endswith("⠄⠾"):
                    treated_word = treated_word[:-2]

                is_upper_case = False
                if not is_number and word.startswith("⠨⠨"):
                    is_upper_case = True
                    treated_word = treated_word[2:]
                
                last_letter = None
                for letter in treated_word:
                    if letter == "⠠" or letter == "⠨":
                        last_letter = letter
                        continue

                    if letter == "⠂" and last_letter == "⠠":
                        text += "/"
                        continue

                    if letter == "⠴" and last_letter == "⠸":
                        text += "%"
                        continue

                    if is_number and letter == "⠂":
                        is_number = False
                        continue
                    
                    index_of_letter = -1
                    try:
                        index_of_letter = BRAZILIAN.braille.index(letter)
                    except:
                        last_letter = letter
                        continue

                    if is_number:
                        index_of_letter = (BRAZILIAN.braille[38:]).index(letter) + 38
                    
                    if is_upper_case or last_letter == "⠨":
                        text += BRAZILIAN.normal[index_of_letter].upper()
                    else:
                        text += BRAZILIAN.normal[index_of_letter]

                    last_letter = letter

                if word.endswith("⠄⠜"):
                    text += ")"

                if word.endswith("⠄⠾"):
                    text += "]"

            except:
                pass
            
            text += " "

        text = text.rstrip() + "\n"

    return text.rstrip()


# --- Chinese (Mandarin) Decoding ---

_YU_FINALS = {"ü": "u", "üe": "ue", "üan": "uan", "ün": "un"}
_I_OR_YU_START = ("i", "ü")


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

    # Disambiguate final cell ⠢ (o vs e) based on phonotactics
    if final == "o" and initial not in ("", "b", "p", "m", "f"):
        final = "e"

    return initial + final + tone


def decode_chinese(braille: str) -> str:
    lines = braille.split("\n")
    return "\n".join(_decode_line(line) for line in lines)