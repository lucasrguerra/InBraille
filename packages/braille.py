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



def characterTo3d(character, radius=1, spacing=2.7, resolution=20, points_only=False):
    def points(code):
        return stl.createBraillePoints(code, radius, spacing, resolution, points_only, Rules.dots_apparent_thickness)

    braille_characters_3d = {
        "⠁": points("100000"),   # ⠁
        "⠃": points("110000"),   # ⠃
        "⠉": points("100100"),   # ⠉
        "⠙": points("100110"),   # ⠙
        "⠑": points("100010"),   # ⠑
        "⠋": points("110100"),   # ⠋
        "⠛": points("110110"),   # ⠛
        "⠓": points("110010"),   # ⠓
        "⠊": points("010100"),   # ⠊
        "⠚": points("010110"),   # ⠚
        "⠅": points("101000"),   # ⠅
        "⠇": points("111000"),   # ⠇
        "⠍": points("101100"),   # ⠍

        "⠝": points("101110"),   # ⠝
        "⠕": points("101010"),   # ⠕
        "⠏": points("111100"),   # ⠏
        "⠟": points("111110"),   # ⠟
        "⠗": points("111010"),   # ⠗
        "⠎": points("011100"),   # ⠎
        "⠞": points("011110"),   # ⠞
        "⠥": points("101001"),   # ⠥
        "⠧": points("111001"),   # ⠧
        "⠺": points("010111"),   # ⠺
        "⠭": points("101101"),   # ⠭
        "⠽": points("101111"),   # ⠽
        "⠵": points("101011"),   # ⠵

        "⠴": points("001011"),   # ⠴
        "⠂": points("010000"),   # ⠂
        "⠆": points("011000"),   # ⠆
        "⠒": points("010010"),   # ⠒
        "⠲": points("010011"),   # ⠲
        "⠢": points("010001"),   # ⠢
        "⠖": points("011010"),   # ⠖
        "⠶": points("011011"),   # ⠶
        "⠦": points("011001"),   # ⠦
        "⠔": points("001010"),   # ⠔

        "⠮": points("011101"),   # ⠮
        "⠹": points("100111"),   # ⠹
        "⠯": points("111101"),   # ⠯
        "⠫": points("110101"),   # ⠫
        "⠼": points("001111"),   # ⠼
        "⠈": points("000100"),   # ⠈
        "⠩": points("100101"),   # ⠩
        "⠷": points("111011"),   # ⠷
        "⠾": points("011111"),   # ⠾
        "⠪": points("010101"),   # ⠪
        "⠻": points("110111"),   # ⠻
        "⠸": points("000111"),   # ⠸

        "⠬": points("001101"),   # ⠬
        "⠤": points("001001"),   # ⠤
        "⠡": points("100001"),   # ⠡
        "⠌": points("001100"),   # ⠌
        "⠿": points("111111"),   # ⠿
        "⠣": points("110001"),   # ⠣
        "⠜": points("001110"),   # ⠜
        "⠨": points("000101"),   # ⠨
        "⠠": points("000001"),   # ⠠
        "⠰": points("000011"),   # ⠰
        "⠱": points("100011"),   # ⠱

        "⠄": points("001000"),   # ⠄
        "⠐": points("000010"),   # ⠐

        "⣄": points("011001"),   # ⣄
    }

    return braille_characters_3d[character]



def _cornerMarker(corner_x, corner_y, plate_thickness, resolution):
    # A raised dot (slightly larger than a braille dot) placed on top of the plate,
    # inset from the given bottom-left corner, to indicate the correct orientation.
    inset = 3.0
    marker_radius = 1.6
    marker = stl.createBrailleCap(marker_radius, Rules.dots_apparent_thickness, resolution)
    return stl.makeTranslation(marker, corner_x + inset, corner_y + inset, plate_thickness)



def toSTL(
        braille,
        resolution=20,
        plate_thickness=2,
        unique_plate=False,
        symbols_per_line=20,
        text_alignment="left",
        rounded=False,
        points_only=False
    ):

    scene = stl.createScene()

    if points_only:
        # No plate is generated: caps rest on z=0, the layout is single-block and
        # plate-related options (separate plates / rounded borders) don't apply.
        unique_plate = True
        rounded = False

    phrases = braille.split("\n")
    number_of_phrases = len(phrases)
    plate_width = ((symbols_per_line - 1) * Rules.cells_h_spacing) + Rules.cells_width
    letter_reference_z = 0 if points_only else (plate_thickness - (Rules.dots_radius - Rules.dots_apparent_thickness))
    reference_z = plate_thickness / 2
    plate_height = Rules.cells_v_spacing
    border_size = Rules.cells_width
    border_cylinder = stl.createCylinder(border_size, plate_thickness, resolution)
    border_cylinder_x_reference = (border_size - 0.7) - border_size
    border_plate_x_reference = -(0.7 + (border_size / 2))

    for phrase_index, phrase in enumerate(phrases):
        phrase_scene = stl.createScene()
        this_phrase_width = ((len(phrase) - 1) * Rules.cells_h_spacing) + Rules.cells_width

        if not unique_plate:
            this_plate_height = Rules.cells_v_spacing * 2
            
            plate_position_x = plate_width / 2
            plate_position_y = ((plate_height - Rules.cells_height) / 2)

            final_plate_width = plate_width + Rules.cells_v_spacing
            this_plate = stl.createPlate(final_plate_width, this_plate_height, plate_thickness)
            phrase_scene.AddInputData(stl.makeTranslation(this_plate, plate_position_x, plate_position_y, reference_z))

            # Orientation marker: a raised dot on the bottom-left corner of the plate.
            phrase_scene.AddInputData(_cornerMarker(
                plate_position_x - (final_plate_width / 2),
                plate_position_y - (this_plate_height / 2),
                plate_thickness,
                resolution
            ))

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
            if unique_plate:
                letter_position_y -= (phrase_index * Rules.cells_v_spacing)

            if text_alignment == "center":
                letter_position_x += (plate_width - this_phrase_width) / 2
            elif text_alignment == "right":
                letter_position_x += (plate_width - this_phrase_width)
            
            letter_in_3d = characterTo3d(letter, Rules.dots_radius, Rules.dots_spacing, resolution, points_only)
            phrase_scene.AddInputData(stl.makeTranslation(letter_in_3d, letter_position_x, letter_position_y, letter_position_z))

        phrase_scene.Update()
        phrase_position_z = phrase_index * (plate_thickness + Rules.cells_v_spacing)
        if unique_plate:
            phrase_position_z = 0
        scene.AddInputData(stl.makeTranslation(phrase_scene.GetOutput(), 0, 0, phrase_position_z))

    if unique_plate and not points_only:
        border_y_reference = (Rules.cells_v_spacing + ((Rules.cells_v_spacing - Rules.cells_height) / 2))
        plate_height = (number_of_phrases * Rules.cells_v_spacing) + Rules.cells_v_spacing
        plate_position_x = plate_width / 2
        plate_position_y = border_y_reference - (plate_height / 2)

        final_plate_width = plate_width + Rules.cells_v_spacing
        plate = stl.createPlate(final_plate_width, plate_height, plate_thickness)
        scene.AddInputData(stl.makeTranslation(plate, plate_position_x, plate_position_y, reference_z))

        # Orientation marker: a raised dot on the bottom-left corner so the plate isn't
        # read/printed upside down.
        scene.AddInputData(_cornerMarker(
            plate_position_x - (final_plate_width / 2),
            plate_position_y - (plate_height / 2),
            plate_thickness,
            resolution
        ))

        if rounded:
            border_plate = stl.createPlate(border_size, (plate_height - (border_size * 2)), plate_thickness)

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
                (border_y_reference - plate_height + border_size),
                reference_z
            ))
            scene.AddInputData(stl.makeTranslation(copy.deepcopy(border_cylinder),
                (border_cylinder_x_reference + final_plate_width),
                (border_y_reference - plate_height + border_size),
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


    if points_only:
        # Add a thin orientation bar below the lowest dots so the user knows which
        # side is "down" and doesn't glue the points upside down.
        scene.Update()
        bounds = scene.GetOutput().GetBounds()
        x_min, x_max, y_min = bounds[0], bounds[1], bounds[2]
        bar_width = x_max - x_min
        if bar_width > 0:
            bar_depth = 1.2
            bar_height = Rules.dots_apparent_thickness
            bar_gap = 0.8
            bar = stl.createPlate(bar_width, bar_depth, bar_height)
            scene.AddInputData(stl.makeTranslation(
                bar,
                (x_min + x_max) / 2,
                y_min - bar_gap - (bar_depth / 2),
                bar_height / 2
            ))

    scene.Update()
    return stl.sceneToSTL(stl.makeTranslation(scene.GetOutput(), 0, 0, 0, 90))