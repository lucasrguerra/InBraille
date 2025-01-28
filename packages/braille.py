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
    border_space = (Rules.cells_v_spacing - Rules.cells_height) / 2
    biggest_phrase = max([len(phrase) for phrase in phrases])
    biggest_plate_width = (Rules.cells_h_spacing * (biggest_phrase - 1)) + Rules.cells_width + border_space
    if not rounded:
        biggest_plate_width += border_space
    plate_height = Rules.cells_v_spacing
    plate_position_z = plate_thickness / 2
    character_position_z = (plate_thickness - (Rules.dots_radius - Rules.dots_apparent_thickness))
    sum_plat_positions_y = 0

    for index_a, phrase in enumerate(phrases):
        plate_width = (Rules.cells_h_spacing * (len(phrase) -1)) + Rules.cells_width + border_space
        if not rounded:
            plate_width += border_space

        plate_margin_x = (biggest_plate_width - plate_width) / 2
        if text_alignment == "right":
            plate_margin_x = biggest_plate_width - plate_width
        if unique_width:
            plate_width = biggest_plate_width

        plate = stl.createPlate(plate_width, plate_height, plate_thickness)
        plate_position_x = (plate_width / 2) - Rules.dots_radius
        if not unique_width and text_alignment != "left" and unique_plate:
            plate_position_x += plate_margin_x

        plate_position_y = (index_a * plate_height) + Rules.dots_radius
        if not unique_plate:
            plate_position_y += (index_a * Rules.cells_height)
        sum_plat_positions_y += plate_position_y

        scene.AddInputData(stl.makeTranslation(plate, plate_position_x, -plate_position_y, plate_position_z))

        for index_b, character in enumerate(phrase):
            if character == "⠀":
                continue
            
            character_3d = characterTo3d(character, Rules.dots_radius, Rules.dots_spacing, resolution)
            character_position_x = (index_b * Rules.cells_h_spacing) + border_space
            if unique_plate or unique_width:
                if text_alignment == "center":
                    character_position_x += ((biggest_phrase - len(phrase)) * Rules.cells_h_spacing) / 2
                elif text_alignment == "right":
                    character_position_x += ((biggest_phrase - len(phrase)) * Rules.cells_h_spacing)

            if rounded:
                character_position_x -= (border_space / 2)

            character_position_y = (index_a * plate_height) + (Rules.cells_height / 2)
            if not unique_plate:
                character_position_y += (index_a * Rules.cells_height)

            character_3d = stl.makeTranslation(character_3d, character_position_x, -character_position_y, character_position_z)
            scene.AddInputData(character_3d)

        if rounded:
            border_size = border_space / 2

            if unique_plate and unique_width:
                border_cylinder = stl.createCylinder(border_size, plate_thickness, resolution)

                if index_a == 0:
                    border_reference_y = (plate_position_y - (plate_height / 2) + border_size)
                    scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder), 0, -border_reference_y, plate_position_z))
                    scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder), plate_width, -border_reference_y, plate_position_z))

                if index_a == (number_of_phrases - 1):
                    border_reference_y = (plate_position_y + (plate_height / 2) - border_size)
                    scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder), 0, -border_reference_y, plate_position_z))
                    scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder), plate_width, -border_reference_y , plate_position_z))

                    border_plate = stl.createPlate(border_size, ((plate_height * number_of_phrases) - (border_size * 2)), plate_thickness)
                    border_plate_position_y = (sum_plat_positions_y / number_of_phrases)
                    scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_plate), -((border_size / 2) + Rules.dots_radius), -border_plate_position_y, plate_position_z))
                    scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_plate), ((plate_width + 0.275) - border_size), -border_plate_position_y, plate_position_z))
            
            if not unique_plate:
                border_cylinder = stl.createCylinder(border_size, plate_thickness, resolution)
                border_plater = stl.createPlate(border_size, (plate_height - border_space), plate_thickness)

                border_reference_top_y = (plate_position_y - (plate_height / 2) + border_size)
                border_reference_bottom_y = border_reference_top_y + (plate_height - border_space)
                scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder), 0, -border_reference_top_y, plate_position_z))
                scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder), plate_width, -border_reference_top_y, plate_position_z))
                scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder), 0, -border_reference_bottom_y, plate_position_z))
                scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder), plate_width, -border_reference_bottom_y, plate_position_z))
                scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_plater), -((border_size / 2) + Rules.dots_radius), -plate_position_y, plate_position_z))
                scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_plater), ((plate_width + 0.275) - border_size), -plate_position_y, plate_position_z))

    scene.Update()
    return stl.sceneToSTL(stl.makeTranslation(scene.GetOutput(), 0, 0, 0, 90))