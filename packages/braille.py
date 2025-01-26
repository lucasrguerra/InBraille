from packages import stl, encoders, decoders



def encode(text, alphabet="NorthAmerican"):
    if alphabet == "North American":
        return encoders.northAmerican(text)
    elif alphabet == "Brazilian":
        return encoders.brazilian(text)
    else:
        return "Alphabet not found."



def decode(braille, alphabet="NorthAmerican"):
    if alphabet == "North American":
        return decoders.northAmerican(braille)
    elif alphabet == "Brazilian":
        return decoders.brazilian(braille)
    else:
        return "Alphabet not found."



def characterTo3d(character, radius, spacing, subdivisions):
    braille_characters_3d = {
        "⠁": stl.createBraillePoints("100000", radius, spacing, subdivisions),   # ⠁
        "⠃": stl.createBraillePoints("110000", radius, spacing, subdivisions),   # ⠃
        "⠉": stl.createBraillePoints("100100", radius, spacing, subdivisions),   # ⠉
        "⠙": stl.createBraillePoints("100110", radius, spacing, subdivisions),   # ⠙
        "⠑": stl.createBraillePoints("100010", radius, spacing, subdivisions),   # ⠑
        "⠋": stl.createBraillePoints("110100", radius, spacing, subdivisions),   # ⠋
        "⠛": stl.createBraillePoints("110110", radius, spacing, subdivisions),   # ⠛
        "⠓": stl.createBraillePoints("110010", radius, spacing, subdivisions),   # ⠓
        "⠊": stl.createBraillePoints("010100", radius, spacing, subdivisions),   # ⠊
        "⠚": stl.createBraillePoints("010110", radius, spacing, subdivisions),   # ⠚
        "⠅": stl.createBraillePoints("101000", radius, spacing, subdivisions),   # ⠅
        "⠇": stl.createBraillePoints("111000", radius, spacing, subdivisions),   # ⠇
        "⠍": stl.createBraillePoints("101100", radius, spacing, subdivisions),   # ⠍

        "⠝": stl.createBraillePoints("101110", radius, spacing, subdivisions),   # ⠝
        "⠕": stl.createBraillePoints("101010", radius, spacing, subdivisions),   # ⠕
        "⠏": stl.createBraillePoints("111100", radius, spacing, subdivisions),   # ⠏
        "⠟": stl.createBraillePoints("111110", radius, spacing, subdivisions),   # ⠟
        "⠗": stl.createBraillePoints("111010", radius, spacing, subdivisions),   # ⠗
        "⠎": stl.createBraillePoints("011100", radius, spacing, subdivisions),   # ⠎
        "⠞": stl.createBraillePoints("011110", radius, spacing, subdivisions),   # ⠞
        "⠥": stl.createBraillePoints("101001", radius, spacing, subdivisions),   # ⠥
        "⠧": stl.createBraillePoints("111001", radius, spacing, subdivisions),   # ⠧
        "⠺": stl.createBraillePoints("010111", radius, spacing, subdivisions),   # ⠺
        "⠭": stl.createBraillePoints("101101", radius, spacing, subdivisions),   # ⠭
        "⠽": stl.createBraillePoints("101111", radius, spacing, subdivisions),   # ⠽
        "⠵": stl.createBraillePoints("101011", radius, spacing, subdivisions),   # ⠵

        "⠴": stl.createBraillePoints("001011", radius, spacing, subdivisions),   # ⠴
        "⠂": stl.createBraillePoints("010000", radius, spacing, subdivisions),   # ⠂
        "⠆": stl.createBraillePoints("011000", radius, spacing, subdivisions),   # ⠆
        "⠒": stl.createBraillePoints("010010", radius, spacing, subdivisions),   # ⠒
        "⠲": stl.createBraillePoints("010011", radius, spacing, subdivisions),   # ⠲
        "⠢": stl.createBraillePoints("010001", radius, spacing, subdivisions),   # ⠢
        "⠖": stl.createBraillePoints("011010", radius, spacing, subdivisions),   # ⠖
        "⠶": stl.createBraillePoints("011011", radius, spacing, subdivisions),   # ⠶
        "⠦": stl.createBraillePoints("011001", radius, spacing, subdivisions),   # ⠦
        "⠔": stl.createBraillePoints("001010", radius, spacing, subdivisions),   # ⠔

        "⠮": stl.createBraillePoints("011101", radius, spacing, subdivisions),   # ⠮
        "⠹": stl.createBraillePoints("100111", radius, spacing, subdivisions),   # ⠹
        "⠯": stl.createBraillePoints("111101", radius, spacing, subdivisions),   # ⠯
        "⠫": stl.createBraillePoints("110101", radius, spacing, subdivisions),   # ⠫
        "⠼": stl.createBraillePoints("001111", radius, spacing, subdivisions),   # ⠼
        "⠈": stl.createBraillePoints("000100", radius, spacing, subdivisions),   # ⠈
        "⠩": stl.createBraillePoints("100101", radius, spacing, subdivisions),   # ⠩
        "⠷": stl.createBraillePoints("111011", radius, spacing, subdivisions),   # ⠷
        "⠾": stl.createBraillePoints("011111", radius, spacing, subdivisions),   # ⠾
        "⠪": stl.createBraillePoints("010101", radius, spacing, subdivisions),   # ⠪
        "⠻": stl.createBraillePoints("110111", radius, spacing, subdivisions),   # ⠻
        "⠸": stl.createBraillePoints("000111", radius, spacing, subdivisions),   # ⠸

        "⠬": stl.createBraillePoints("001101", radius, spacing, subdivisions),   # ⠬
        "⠤": stl.createBraillePoints("001001", radius, spacing, subdivisions),   # ⠤
        "⠡": stl.createBraillePoints("100001", radius, spacing, subdivisions),   # ⠡
        "⠌": stl.createBraillePoints("001100", radius, spacing, subdivisions),   # ⠌
        "⠿": stl.createBraillePoints("111111", radius, spacing, subdivisions),   # ⠿
        "⠣": stl.createBraillePoints("110001", radius, spacing, subdivisions),   # ⠣
        "⠜": stl.createBraillePoints("001110", radius, spacing, subdivisions),   # ⠜
        "⠨": stl.createBraillePoints("000101", radius, spacing, subdivisions),   # ⠨
        "⠠": stl.createBraillePoints("000001", radius, spacing, subdivisions),   # ⠠
        "⠰": stl.createBraillePoints("000011", radius, spacing, subdivisions),   # ⠰
        "⠱": stl.createBraillePoints("100011", radius, spacing, subdivisions),   # ⠱

        "⠄": stl.createBraillePoints("001000", radius, spacing, subdivisions),   # ⠄
        "⠐": stl.createBraillePoints("000010", radius, spacing, subdivisions),   # ⠐

        "⣄": stl.createBraillePoints("011001", radius, spacing, subdivisions),   # ⣄
    }

    return braille_characters_3d[character]



def toSTL(
        braille,
        radius=0.7,
        spacing=2.2,
        kerning=2.8,
        subdivisions=2,
        thickness=1,
        unique_plate=False,
        unique_width=False,
        text_alignment="left",
        rounded=False
    ):
    scene = stl.createScene()

    phrases = braille.split("\n")
    number_of_phrases = len(phrases)
    biggest_phrase = max(phrases, key=len)
    plate_width = 0
    plate_height = 0

    for index_a, phrase in enumerate(phrases):
        plate_reference = (len(phrase) * (spacing * kerning)) + spacing
        plate_width = plate_reference
        if unique_width:
            plate_width = (len(biggest_phrase) * (spacing * kerning)) + spacing
        if rounded:
            plate_width -= spacing / 2

        plate_height = (spacing * 4)
        plate = stl.createPlate(plate_width, plate_height, thickness)

        position_y = -((spacing * 5) * index_a)
        if unique_plate:
            position_y = -((spacing * 4) * index_a)

        if text_alignment == "left":
            scene.add_geometry(plate.apply_translation([(plate_width / 2), (-spacing + position_y), 0]))
        elif text_alignment == "center":
            scene.add_geometry(plate.apply_translation([0, (-spacing + position_y), 0]))
        elif text_alignment == "right":
            scene.add_geometry(plate.apply_translation([(-plate_width / 2), (-spacing + position_y), 0]))

        position_x = 0
        for index_b, character in enumerate(phrase):
            if text_alignment == "left":
                position_x = (index_b + 0.5) * (spacing * kerning)
            elif text_alignment == "center":
                position_x = (index_b + 0.5) * (spacing * kerning) - (plate_reference / 2)
            elif text_alignment == "right":
                position_x = (index_b + 0.5) * (spacing * kerning) - plate_reference

            if character != " ":
                try:
                    character_3d = characterTo3d(character, radius, spacing, subdivisions)
                    scene.add_geometry(character_3d.apply_translation([position_x, position_y, ((thickness / radius) - (thickness * 0.94))]))
                except:
                    pass
        
        if rounded:
            border_cylinder = stl.createCylinder((radius * 1.14), thickness)
            border_size = spacing / 1.38
            border_plate = stl.createPlate(border_size, (plate_height - (spacing / 1.3)), thickness)

            if not unique_plate:
                if text_alignment == "left":
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([0, (position_y + (kerning / 2)), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([plate_width, (position_y + (kerning / 2)), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([0, (position_y - (kerning * 1.035) * 2), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([plate_width , (position_y - (kerning * 1.035) * 2), 0]))
                    scene.add_geometry((border_plate.__copy__()).apply_translation([0, (-spacing + position_y), 0]))
                    scene.add_geometry((border_plate.__copy__()).apply_translation([plate_width, (-spacing + position_y), 0]))

                elif text_alignment == "center":
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([-(plate_width / 2), (position_y + (kerning / 2)), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([(plate_width / 2), (position_y + (kerning / 2)), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([-(plate_width / 2), (position_y - (kerning * 1.035) * 2), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([(plate_width / 2), (position_y - (kerning * 1.035) * 2), 0]))
                    scene.add_geometry((border_plate.__copy__()).apply_translation([-(plate_width / 2), (-spacing + position_y), 0]))
                    scene.add_geometry((border_plate.__copy__()).apply_translation([(plate_width / 2), (-spacing + position_y), 0]))

                elif text_alignment == "right":
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([-plate_width, (position_y + (kerning / 2)), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([0, (position_y + (kerning / 2)), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([-plate_width, (position_y - (kerning * 1.035) * 2), 0]))
                    scene.add_geometry((border_cylinder.__copy__()).apply_translation([0 , (position_y - (kerning * 1.035) * 2), 0]))
                    scene.add_geometry((border_plate.__copy__()).apply_translation([-plate_width, (-spacing + position_y), 0]))
                    scene.add_geometry((border_plate.__copy__()).apply_translation([0, (-spacing + position_y), 0]))

                continue

            if unique_plate and unique_width:
                if index_a == 0:
                    if text_alignment == "left":
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([0, (position_y + (kerning / 2)), 0]))
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([plate_width, (position_y + (kerning / 2)), 0]))
                    elif text_alignment == "center":
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([(plate_width / 2), (position_y + (kerning / 2)), 0]))
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([-(plate_width / 2), (position_y + (kerning / 2)), 0]))
                    elif text_alignment == "right":
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([0, (position_y + (kerning / 2)), 0]))
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([-plate_width, (position_y + (kerning / 2)), 0]))
                    
                if index_a == (number_of_phrases - 1):
                    border_plate = stl.createPlate((spacing / 1.38), ((plate_height * number_of_phrases) - (spacing / 1.3)), thickness)
                    border_position_y = (position_y + (spacing * ((2 * number_of_phrases) - 3)))

                    if text_alignment == "left":
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([0, (position_y - (kerning * 1.035) * 2), 0]))
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([plate_width, (position_y - (kerning * 1.035) * 2), 0]))
                        scene.add_geometry((border_plate.__copy__()).apply_translation([0, border_position_y, 0]))
                        scene.add_geometry((border_plate.__copy__()).apply_translation([plate_width, border_position_y, 0]))
                    elif text_alignment == "center":
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([(plate_width / 2), (position_y - (kerning * 1.035) * 2), 0]))
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([-(plate_width / 2), (position_y - (kerning * 1.035) * 2), 0]))
                        scene.add_geometry((border_plate.__copy__()).apply_translation([(plate_width / 2), border_position_y, 0]))
                        scene.add_geometry((border_plate.__copy__()).apply_translation([-(plate_width / 2), border_position_y, 0]))
                    elif text_alignment == "right":
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([0, (position_y - (kerning * 1.035) * 2), 0]))
                        scene.add_geometry((border_cylinder.__copy__()).apply_translation([-plate_width, (position_y - (kerning * 1.035) * 2), 0]))
                        scene.add_geometry((border_plate.__copy__()).apply_translation([0, border_position_y, 0]))
                        scene.add_geometry((border_plate.__copy__()).apply_translation([-plate_width, border_position_y, 0]))

                continue

    return stl.sceneToSTL(scene)