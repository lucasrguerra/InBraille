from packages import stl, encoders, decoders
import copy



class Rules:
    dots_radius = 1
    dots_spacing = 2.7
    dots_apparent_thickness = 0.65
    cells_width = 4.7
    cells_height = 7.4
    cells_h_spacing = 6.6
    cells_v_spacing = 10.8


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



def characterTo3d(character, radius=1, spacing=2.7, resolution=20):
    braille_characters_3d = {
        "⠁": stl.createBraillePoints("100000", radius, spacing, resolution),   # ⠁
        "⠃": stl.createBraillePoints("110000", radius, spacing, resolution),   # ⠃
        "⠉": stl.createBraillePoints("100100", radius, spacing, resolution),   # ⠉
        "⠙": stl.createBraillePoints("100110", radius, spacing, resolution),   # ⠙
        "⠑": stl.createBraillePoints("100010", radius, spacing, resolution),   # ⠑
        "⠋": stl.createBraillePoints("110100", radius, spacing, resolution),   # ⠋
        "⠛": stl.createBraillePoints("110110", radius, spacing, resolution),   # ⠛
        "⠓": stl.createBraillePoints("110010", radius, spacing, resolution),   # ⠓
        "⠊": stl.createBraillePoints("010100", radius, spacing, resolution),   # ⠊
        "⠚": stl.createBraillePoints("010110", radius, spacing, resolution),   # ⠚
        "⠅": stl.createBraillePoints("101000", radius, spacing, resolution),   # ⠅
        "⠇": stl.createBraillePoints("111000", radius, spacing, resolution),   # ⠇
        "⠍": stl.createBraillePoints("101100", radius, spacing, resolution),   # ⠍

        "⠝": stl.createBraillePoints("101110", radius, spacing, resolution),   # ⠝
        "⠕": stl.createBraillePoints("101010", radius, spacing, resolution),   # ⠕
        "⠏": stl.createBraillePoints("111100", radius, spacing, resolution),   # ⠏
        "⠟": stl.createBraillePoints("111110", radius, spacing, resolution),   # ⠟
        "⠗": stl.createBraillePoints("111010", radius, spacing, resolution),   # ⠗
        "⠎": stl.createBraillePoints("011100", radius, spacing, resolution),   # ⠎
        "⠞": stl.createBraillePoints("011110", radius, spacing, resolution),   # ⠞
        "⠥": stl.createBraillePoints("101001", radius, spacing, resolution),   # ⠥
        "⠧": stl.createBraillePoints("111001", radius, spacing, resolution),   # ⠧
        "⠺": stl.createBraillePoints("010111", radius, spacing, resolution),   # ⠺
        "⠭": stl.createBraillePoints("101101", radius, spacing, resolution),   # ⠭
        "⠽": stl.createBraillePoints("101111", radius, spacing, resolution),   # ⠽
        "⠵": stl.createBraillePoints("101011", radius, spacing, resolution),   # ⠵

        "⠴": stl.createBraillePoints("001011", radius, spacing, resolution),   # ⠴
        "⠂": stl.createBraillePoints("010000", radius, spacing, resolution),   # ⠂
        "⠆": stl.createBraillePoints("011000", radius, spacing, resolution),   # ⠆
        "⠒": stl.createBraillePoints("010010", radius, spacing, resolution),   # ⠒
        "⠲": stl.createBraillePoints("010011", radius, spacing, resolution),   # ⠲
        "⠢": stl.createBraillePoints("010001", radius, spacing, resolution),   # ⠢
        "⠖": stl.createBraillePoints("011010", radius, spacing, resolution),   # ⠖
        "⠶": stl.createBraillePoints("011011", radius, spacing, resolution),   # ⠶
        "⠦": stl.createBraillePoints("011001", radius, spacing, resolution),   # ⠦
        "⠔": stl.createBraillePoints("001010", radius, spacing, resolution),   # ⠔

        "⠮": stl.createBraillePoints("011101", radius, spacing, resolution),   # ⠮
        "⠹": stl.createBraillePoints("100111", radius, spacing, resolution),   # ⠹
        "⠯": stl.createBraillePoints("111101", radius, spacing, resolution),   # ⠯
        "⠫": stl.createBraillePoints("110101", radius, spacing, resolution),   # ⠫
        "⠼": stl.createBraillePoints("001111", radius, spacing, resolution),   # ⠼
        "⠈": stl.createBraillePoints("000100", radius, spacing, resolution),   # ⠈
        "⠩": stl.createBraillePoints("100101", radius, spacing, resolution),   # ⠩
        "⠷": stl.createBraillePoints("111011", radius, spacing, resolution),   # ⠷
        "⠾": stl.createBraillePoints("011111", radius, spacing, resolution),   # ⠾
        "⠪": stl.createBraillePoints("010101", radius, spacing, resolution),   # ⠪
        "⠻": stl.createBraillePoints("110111", radius, spacing, resolution),   # ⠻
        "⠸": stl.createBraillePoints("000111", radius, spacing, resolution),   # ⠸

        "⠬": stl.createBraillePoints("001101", radius, spacing, resolution),   # ⠬
        "⠤": stl.createBraillePoints("001001", radius, spacing, resolution),   # ⠤
        "⠡": stl.createBraillePoints("100001", radius, spacing, resolution),   # ⠡
        "⠌": stl.createBraillePoints("001100", radius, spacing, resolution),   # ⠌
        "⠿": stl.createBraillePoints("111111", radius, spacing, resolution),   # ⠿
        "⠣": stl.createBraillePoints("110001", radius, spacing, resolution),   # ⠣
        "⠜": stl.createBraillePoints("001110", radius, spacing, resolution),   # ⠜
        "⠨": stl.createBraillePoints("000101", radius, spacing, resolution),   # ⠨
        "⠠": stl.createBraillePoints("000001", radius, spacing, resolution),   # ⠠
        "⠰": stl.createBraillePoints("000011", radius, spacing, resolution),   # ⠰
        "⠱": stl.createBraillePoints("100011", radius, spacing, resolution),   # ⠱

        "⠄": stl.createBraillePoints("001000", radius, spacing, resolution),   # ⠄
        "⠐": stl.createBraillePoints("000010", radius, spacing, resolution),   # ⠐

        "⣄": stl.createBraillePoints("011001", radius, spacing, resolution),   # ⣄
    }

    return braille_characters_3d[character]



def toSTL(
        braille,
        resolution=20,
        plate_thickness=2,
        unique_plate=False,
        unique_width=False,
        text_alignment="left",
        rounded=False
    ):

    scene = stl.createScene()

    phrases = braille.split("\n")
    number_of_phrases = len(phrases)
    biggest_phrase = max([len(phrase) for phrase in phrases])
    biggest_phrase_width = ((biggest_phrase - 1) * Rules.cells_h_spacing) + Rules.cells_width
    letter_reference_z = (plate_thickness - (Rules.dots_radius - Rules.dots_apparent_thickness))
    reference_z = plate_thickness / 2
    plate_height = Rules.cells_v_spacing
    border_size = Rules.cells_width
    border_cylinder = stl.createCylinder(border_size, plate_thickness, resolution)
    border_cylinder_x_reference = (0.3 - border_size)
    border_plate_x_reference = -(0.7 + (border_size / 2))

    for phrase_index, phrase in enumerate(phrases):
        phrase_scene = stl.createScene()
        this_phrase_width = ((len(phrase) - 1) * Rules.cells_h_spacing) + Rules.cells_width

        if not unique_plate:
            this_plate_height = Rules.cells_v_spacing * 2
            this_plate_width = this_phrase_width
            if unique_width:
                this_plate_width = biggest_phrase_width
            
            plate_position_x = this_plate_width / 2
            plate_position_y = ((plate_height - Rules.cells_height) / 2)

            final_plate_width = this_plate_width + Rules.cells_v_spacing
            this_plate = stl.createPlate(final_plate_width, this_plate_height, plate_thickness)
            phrase_scene.AddInputData(stl.makeTranslation(this_plate, plate_position_x, plate_position_y, reference_z))

            if rounded:
                half_plate_height = this_plate_height / 2
                border_plate = stl.createPlate(border_size, (this_plate_height - (border_size * 2)), plate_thickness)

                phrase_scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                    border_cylinder_x_reference,
                    (plate_position_y + half_plate_height - border_size),
                    reference_z
                ))
                phrase_scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                    border_cylinder_x_reference + final_plate_width,
                    (plate_position_y + half_plate_height - border_size),
                    reference_z
                ))
                phrase_scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                    border_cylinder_x_reference,
                    (plate_position_y - half_plate_height + border_size),
                    reference_z
                ))
                phrase_scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                    border_cylinder_x_reference + final_plate_width,
                    (plate_position_y - half_plate_height + border_size),
                    reference_z
                ))
                phrase_scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_plate),
                    (border_plate_x_reference - border_size),
                    plate_position_y,
                    reference_z
                ))
                phrase_scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_plate),
                    (border_plate_x_reference + final_plate_width),
                    plate_position_y,
                    reference_z
                ))

        for letter_index, letter in enumerate(phrase):
            if letter == "⠀":
                continue

            letter_position_y = -(Rules.dots_radius)
            letter_position_x = (letter_index * Rules.cells_h_spacing) + Rules.dots_radius
            letter_position_z = letter_reference_z
            if unique_plate or unique_width:
                if unique_plate:
                    letter_position_y -= (phrase_index * Rules.cells_v_spacing)

                if text_alignment == "center":
                    letter_position_x += (biggest_phrase_width - this_phrase_width) / 2
                elif text_alignment == "right":
                    letter_position_x += (biggest_phrase_width - this_phrase_width)
            
            letter_in_3d = characterTo3d(letter, Rules.dots_radius, Rules.dots_spacing, resolution)
            phrase_scene.AddInputData(stl.makeTranslation(letter_in_3d, letter_position_x, letter_position_y, letter_position_z))

        phrase_scene.Update()
        phrase_position_z = phrase_index * (plate_thickness + Rules.cells_v_spacing)
        if unique_plate:
            phrase_position_z = 0
        scene.AddInputData(stl.makeTranslation(phrase_scene.GetOutput(), 0, 0, phrase_position_z))

    if unique_plate:
        plate_height = (number_of_phrases * Rules.cells_v_spacing)
        plate_width = biggest_phrase_width
        plate_position_x = plate_width / 2
        plate_position_y = -((plate_height / number_of_phrases) - ((Rules.cells_v_spacing - Rules.cells_height) / 2))

        final_plate_width = plate_width + Rules.cells_v_spacing
        final_plate_height = plate_height + Rules.cells_v_spacing
        plate = stl.createPlate(final_plate_width, final_plate_height, plate_thickness)
        scene.AddInputData(stl.makeTranslation(plate, plate_position_x, plate_position_y, reference_z))

        if rounded:
            border_y_reference = (Rules.cells_v_spacing + ((Rules.cells_v_spacing - Rules.cells_height) / 2))
            border_plate = stl.createPlate(border_size, (final_plate_height - (border_size * 2)), plate_thickness)

            scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                border_cylinder_x_reference,
                (border_y_reference - border_size),
                reference_z
            ))
            scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                (border_cylinder_x_reference + final_plate_width),
                (border_y_reference - border_size),
                reference_z
            ))
            scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                border_cylinder_x_reference,
                (border_y_reference - final_plate_height + border_size),
                reference_z
            ))
            scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                (border_cylinder_x_reference + final_plate_width),
                (border_y_reference - final_plate_height + border_size),
                reference_z
            ))
            scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_plate),
                (border_plate_x_reference - border_size),
                plate_position_y,
                reference_z
            ))
            scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_plate),
                (border_plate_x_reference + final_plate_width),
                plate_position_y,
                reference_z
            ))


    scene.Update()
    return stl.sceneToSTL(stl.makeTranslation(scene.GetOutput(), 0, 0, 0, 90))