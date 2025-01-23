from packages import stl
from io import BytesIO
import trimesh

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

def encode(text):
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
                
                if letter.isalpha() and is_number:
                    text_in_braille += "⠨"
                    is_number = False

                if text_in_braille != "" and not text_in_braille.endswith(" "):
                    if letter == "(" or letter == ")":
                        text_in_braille += " "

                index_of_letter = ascii_characters.index(letter.lower())
                if index_of_letter > -1:
                    if letter != letter.lower() and not text_in_braille.endswith("⠨"):
                        text_in_braille += "⠨"
                    text_in_braille += braille_characters[index_of_letter]
                
                if letter == "(" or letter == ")":
                    text_in_braille += " "
            text_in_braille += " "

        text_in_braille = text_in_braille.rstrip() + "\n"

    return text_in_braille.rstrip()

def decode(text):
    text_in_ascii = ""

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
                    text_in_ascii += "•"
                    is_number = False
                elif index_of_letter > -1:
                    if is_number and index_of_letter < 10:
                        if index_of_letter == 9:
                            text_in_ascii += "0"
                        else:
                            text_in_ascii += str(index_of_letter + 1)
                    else:
                        is_number = False
                        if letter == "⠣" and (text_in_ascii[-1]).isalpha():
                            text_in_ascii += "ê"
                        elif letter == "⠜" and (text_in_ascii[-1]).isalpha():
                            text_in_ascii += "ã"
                        else:
                            text_in_ascii += ascii_characters[index_of_letter]
            text_in_ascii += " "

        text_in_ascii = text_in_ascii.rstrip() + "\n"

    text_in_ascii = text_in_ascii.rstrip()
    result = ""
    is_upper_case = False

    for letter in text_in_ascii:
        if letter == "•":
            is_upper_case = True
        elif is_upper_case:
            result += letter.upper()
            is_upper_case = False
        elif letter == " " and not result.endswith(" "):
            if result.endswith("("):
                pass
            else:
                result += letter
        elif letter == ")" and result.endswith(" "):
            result = result[:-1] + letter
        else:
            result += letter

    return result.replace("•", "")

def characterTo3d(character, size, spacing, subdivisions):
    braille_characters_3d = {
        "⠁": stl.createBrailleCharacter(size, spacing=spacing, subdivisions=subdivisions),                                  # ⠁
        "⠃": stl.createBrailleCharacter(size,0,size, spacing=spacing, subdivisions=subdivisions),                           # ⠃
        "⠉": stl.createBrailleCharacter(size,size, spacing=spacing, subdivisions=subdivisions),                             # ⠉
        "⠙": stl.createBrailleCharacter(size,size,0,size, spacing=spacing, subdivisions=subdivisions),                      # ⠙
        "⠑": stl.createBrailleCharacter(size,0,0,size, spacing=spacing, subdivisions=subdivisions),                         # ⠑
        "⠋": stl.createBrailleCharacter(size,size,size, spacing=spacing, subdivisions=subdivisions),                        # ⠋
        "⠛": stl.createBrailleCharacter(size,size,size,size, spacing=spacing, subdivisions=subdivisions),                   # ⠛
        "⠓": stl.createBrailleCharacter(size,0,size,size, spacing=spacing, subdivisions=subdivisions),                      # ⠓
        "⠊": stl.createBrailleCharacter(0,size,size, spacing=spacing, subdivisions=subdivisions),                           # ⠊
        "⠚": stl.createBrailleCharacter(0,size,size,size, spacing=spacing, subdivisions=subdivisions),                      # ⠚
        "⠅": stl.createBrailleCharacter(size,0,0,0,size, spacing=spacing, subdivisions=subdivisions),                       # ⠅
        "⠇": stl.createBrailleCharacter(size,0,size,0,size, spacing=spacing, subdivisions=subdivisions),                    # ⠇
        "⠍": stl.createBrailleCharacter(size,size,0,0,size, spacing=spacing, subdivisions=subdivisions),                    # ⠍
        "⠝": stl.createBrailleCharacter(size,size,0,size,size, spacing=spacing, subdivisions=subdivisions),                 # ⠝
        "⠕": stl.createBrailleCharacter(size,0,0,size,size, spacing=spacing, subdivisions=subdivisions),                    # ⠕
        "⠏": stl.createBrailleCharacter(size,size,size,0,size, spacing=spacing, subdivisions=subdivisions),                 # ⠏
        "⠟": stl.createBrailleCharacter(size,size,size,size,size, spacing=spacing, subdivisions=subdivisions),              # ⠟
        "⠗": stl.createBrailleCharacter(size,0,size,size,size,0, spacing=spacing, subdivisions=subdivisions),               # ⠗
        "⠎": stl.createBrailleCharacter(0,size,size,0,size, spacing=spacing, subdivisions=subdivisions),                    # ⠎
        "⠞": stl.createBrailleCharacter(0,size,size,size,size, spacing=spacing, subdivisions=subdivisions),                 # ⠞
        "⠥": stl.createBrailleCharacter(size,0,0,0,size,size, spacing=spacing, subdivisions=subdivisions),                  # ⠥
        "⠧": stl.createBrailleCharacter(size,0,size,0,size,size, spacing=spacing, subdivisions=subdivisions),               # ⠧
        "⠺": stl.createBrailleCharacter(0,size,size,size,0,size, spacing=spacing, subdivisions=subdivisions),               # ⠺
        "⠭": stl.createBrailleCharacter(size,size,0,0,size,size, spacing=spacing, subdivisions=subdivisions),               # ⠭
        "⠽": stl.createBrailleCharacter(size,size,0,size,size,size, spacing=spacing, subdivisions=subdivisions),            # ⠽
        "⠵": stl.createBrailleCharacter(size,0,0,size,size,size, spacing=spacing, subdivisions=subdivisions),               # ⠵
        "⠂": stl.createBrailleCharacter(0,0,size, spacing=spacing, subdivisions=subdivisions),                              # ⠂
        "⠆": stl.createBrailleCharacter(0,0,size,0,size, spacing=spacing, subdivisions=subdivisions),                       # ⠆
        "⠒": stl.createBrailleCharacter(0,0,size,size, spacing=spacing, subdivisions=subdivisions),                         # ⠒
        "⠄": stl.createBrailleCharacter(0,0,0,0,size, spacing=spacing, subdivisions=subdivisions),                          # ⠄
        "⠖": stl.createBrailleCharacter(0,0,size,size,size, spacing=spacing, subdivisions=subdivisions),                    # ⠖
        "⠢": stl.createBrailleCharacter(0,0,size,0,0,size, spacing=spacing, subdivisions=subdivisions),                     # ⠢
        "⠶": stl.createBrailleCharacter(0,0,size,size,size,size, spacing=spacing, subdivisions=subdivisions),               # ⠶
        "⠱": stl.createBrailleCharacter(size,0,0,size,0,size, spacing=spacing, subdivisions=subdivisions),                  # ⠱
        "⠠": stl.createBrailleCharacter(0,0,0,0,0,size, spacing=spacing, subdivisions=subdivisions),                        # ⠠
        "⠯": stl.createBrailleCharacter(size,size,size,0,size,size, spacing=spacing, subdivisions=subdivisions),            # ⠯
        "⠷": stl.createBrailleCharacter(size,0,size,size,size,size, spacing=spacing, subdivisions=subdivisions),            # ⠷
        "⠫": stl.createBrailleCharacter(size,size,size,0,0,size, spacing=spacing, subdivisions=subdivisions),               # ⠫
        "⠜": stl.createBrailleCharacter(0,size,0,size,size, spacing=spacing, subdivisions=subdivisions),                    # ⠜
        "⠡": stl.createBrailleCharacter(size,0,0,0,0,size, spacing=spacing, subdivisions=subdivisions),                     # ⠡
        "⠿": stl.createBrailleCharacter(size,size,size,size,size,size, spacing=spacing, subdivisions=subdivisions),         # ⠿
        "⠣": stl.createBrailleCharacter(size,0,size,0,0,size, spacing=spacing, subdivisions=subdivisions),                  # ⠣
        "⠌": stl.createBrailleCharacter(0,size,0,0,size, spacing=spacing, subdivisions=subdivisions),                       # ⠌
        "⠬": stl.createBrailleCharacter(0,size,0,0,size,size, spacing=spacing, subdivisions=subdivisions),                  # ⠬
        "⠹": stl.createBrailleCharacter(size,size,0,size,0,size, spacing=spacing, subdivisions=subdivisions),               # ⠹
        "⠪": stl.createBrailleCharacter(0,size,size,0,0,size, spacing=spacing, subdivisions=subdivisions),                  # ⠪
        "⠾": stl.createBrailleCharacter(0,size,size,size,size,size, spacing=spacing, subdivisions=subdivisions),            # ⠾
        "⠼": stl.createBrailleCharacter(0,size,0,size,size,size, spacing=spacing, subdivisions=subdivisions),               # ⠼
        "⠨": stl.createBrailleCharacter(0,size,0,0,0,size, spacing=spacing, subdivisions=subdivisions),                     # ⠨
        "⣄": stl.createBrailleCharacter(0,0,0,size,size,size, spacing=spacing, subdivisions=subdivisions),                  # ⣄
    }

    return braille_characters_3d[character]

def toSTL(
        text,
        size=2,
        spacing=5,
        kerning=2.5,
        subdivisions=2,
        surface_depth=2,
        unique_surface=False,
        unique_width=False,
        text_alignment="left"
    ):
    scene = trimesh.Scene()

    phrases = text.split("\n")
    biggest_phrase = max(phrases, key=len)

    for index_a, phrase in enumerate(phrases):
        surface_reference = (len(phrase) * (spacing * kerning)) + spacing
        surface_width = surface_reference
        if unique_width:
            surface_width = (len(biggest_phrase) * (spacing * kerning)) + spacing

        surface_height = (spacing * 4)
        surface = stl.createSurface(surface_width, surface_height, surface_depth)

        position_y = -((spacing * 5) * index_a)
        if unique_surface:
            position_y = -((spacing * 4) * index_a)

        if text_alignment == "left":
            scene.add_geometry(surface.apply_translation([(surface_width / 2), (-spacing + position_y), 0]))
        elif text_alignment == "center":
            scene.add_geometry(surface.apply_translation([0, (-spacing + position_y), 0]))
        elif text_alignment == "right":
            scene.add_geometry(surface.apply_translation([(-surface_width / 2), (-spacing + position_y), 0]))

        for index_b, character in enumerate(phrase):
            if text_alignment == "left":
                position_x = (index_b + 0.5) * (spacing * kerning)
            elif text_alignment == "center":
                position_x = (index_b + 0.5) * (spacing * kerning) - (surface_reference / 2)
            elif text_alignment == "right":
                position_x = (index_b + 0.5) * (spacing * kerning) - surface_reference

            if character != " ":
                try:
                    character_3d = characterTo3d(character, size, spacing, subdivisions)
                    scene.add_geometry(character_3d.apply_translation([position_x, position_y, (surface_depth / 2)]))
                except:
                    pass

    data = scene.export(None, "stl")
    file = BytesIO(data)
    file.seek(0)
    return file