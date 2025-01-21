ascii_characters = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
	"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
	"0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ".", ",", "?", ";", ":", "%", "(", ")",
	"!", "=", "@", '"', "ç", "á", "à", "ã", "â", "é", "ê",
    "í", "ó", "ô", "õ", "ú"
]

braille_characters = [
    "⠁", "⠃", "⠉", "⠙", "⠑", "⠋", "⠛", "⠓", "⠊", "⠚", "⠅", "⠇", "⠍",
	"⠝", "⠕", "⠏", "⠟", "⠗", "⠎", "⠞", "⠥", "⠧", "⠺", "⠭", "⠽", "⠵",
	"⠚", "⠁", "⠃", "⠉", "⠙", "⠑", "⠋", "⠛", "⠓", "⠊",
    "⡀", "⠂", "⠢", "⠆", "⠒", "⠸⠴", "⠣", "⠜",
	"⠖", "⠶", "⠱", "⣄", "⠯", "⠷", "⠫", "⠜", "⠡", "⠿", "⠣",
	"⠌", "⠬", "⠹", "⠪", "⠾"
]

def text_to_braille(text):
    text_in_braille = ""

    phrases = text.split("\n")
    for phrase in phrases:
        words = phrase.replace('"', "'").split(" ")
        for word in words:
            first_letter = word[0] if word else ""
            is_number = False
            if first_letter.isdigit():
                text_in_braille += "⠼"
                is_number = True

            for letter in word:
                if not is_number and letter.isdigit():
                    text_in_braille += "⠼"
                    is_number = True

                if is_number and not letter.isdigit():
                    text_in_braille += "⠨"

                index_of_letter = ascii_characters.index(letter.lower()) if letter.lower() in ascii_characters else -1
                if index_of_letter > -1:
                    if letter != letter.lower():
                        text_in_braille += "⠨"
                    text_in_braille += braille_characters[index_of_letter]
            text_in_braille += " "

        text_in_braille = text_in_braille.rstrip() + "\n"

    return text_in_braille.rstrip()

def braille_to_text(text):
    text_in_text = ""

    phrases = text.split("\n")
    for phrase in phrases:
        words = phrase.replace('"', "'").split(" ")
        for word in words:
            is_number = word.startswith("⠼")

            for letter in word:
                if not is_number and letter == "⠼":
                    is_number = True

                index_of_letter = braille_characters.index(letter) if letter in braille_characters else -1
                if letter == "⠨":
                    text_in_text += "*"
                    is_number = False
                elif index_of_letter > -1:
                    if is_number and index_of_letter < 10:
                        text_in_text += "0" if index_of_letter == 9 else str(index_of_letter + 1)
                    else:
                        is_number = False
                        text_in_text += ascii_characters[index_of_letter]
            text_in_text += " "

        text_in_text = text_in_text.rstrip() + "\n"

    text_in_text = text_in_text.rstrip()
    result = []
    is_upper_case = False

    for letter in text_in_text:
        if letter == "*":
            is_upper_case = True
        elif is_upper_case:
            result.append(letter.upper())
            is_upper_case = False
        else:
            result.append(letter)

    return "".join(result).replace("*", "")


def braille_to_points(braille_text, dot_radius=1, dot_spacing=2):
    braille_dots = []
    
    cell_layout = [
        (0, 0), (0, 1),
        (1, 0), (1, 1),
        (2, 0), (2, 1)
    ]

    x_offset = 0

    for char in braille_text:
        if char == '\n':
            x_offset = 0
            braille_dots.append(translate([0, -dot_spacing * 4, 0]))
            continue

        if '\u2800' <= char <= '\u28FF':
            braille_binary = ord(char) - 0x2800
            for i, (dx, dy) in enumerate(cell_layout):
                if braille_binary & (1 << i):
                    dot = translate([
                        x_offset + dx * dot_spacing,
                        -dy * dot_spacing,
                        0
                    ])(sphere(r=dot_radius))
                    braille_dots.append(dot)

        x_offset += dot_spacing * 3

    return union()(*braille_dots)