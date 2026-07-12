"""Builds the 3D mesh of a Braille text: plate, cells, orientation markers and the
points-only orientation bar. Pure geometry composition — it talks only to a MeshEngine,
so it has no knowledge of the underlying 3D library.
"""
from src.domain.braille_codes import BRAILLE_CODES
from src.domain.dimensions import Dimensions
from src.modeling.mesh_engine import MeshEngine
from src.modeling.options import ModelOptions


class BrailleModelBuilder:
    def __init__(self, engine: MeshEngine, dimensions=Dimensions):
        self._engine = engine
        self._dimensions = dimensions

    def build(self, braille: str, options: ModelOptions):
        engine = self._engine
        rules = self._dimensions

        resolution = options.resolution
        plate_thickness = options.plate_thickness
        unique_plate = options.unique_plate
        symbols_per_line = options.symbols_per_line
        text_alignment = options.text_alignment
        rounded = options.rounded
        points_only = options.points_only

        scene = engine.create_scene()

        # Geometry for a given character is identical everywhere it appears, so build each
        # distinct character only once per request and reuse it for every occurrence.
        char_cache = {}

        if points_only:
            # No plate is generated: caps rest on z=0, the layout is single-block and
            # plate-related options (separate plates / rounded borders) don't apply.
            unique_plate = True
            rounded = False

        phrases = braille.split("\n")
        number_of_phrases = len(phrases)
        plate_width = ((symbols_per_line - 1) * rules.cells_h_spacing) + rules.cells_width
        letter_reference_z = 0 if points_only else (plate_thickness - (rules.dots_radius - rules.dots_apparent_thickness))
        reference_z = plate_thickness / 2
        plate_height = rules.cells_v_spacing
        border_size = rules.cells_width
        border_cylinder = engine.create_cylinder(border_size, plate_thickness, resolution)
        border_cylinder_x_reference = (border_size - 0.7) - border_size
        border_plate_x_reference = -(0.7 + (border_size / 2))

        for phrase_index, phrase in enumerate(phrases):
            phrase_scene = engine.create_scene()
            this_phrase_width = ((len(phrase) - 1) * rules.cells_h_spacing) + rules.cells_width

            if not unique_plate:
                this_plate_height = rules.cells_v_spacing * 2

                plate_position_x = plate_width / 2
                plate_position_y = ((plate_height - rules.cells_height) / 2)

                final_plate_width = plate_width + rules.cells_v_spacing
                this_plate = engine.create_plate(final_plate_width, this_plate_height, plate_thickness)
                engine.add(phrase_scene, engine.translate(this_plate, plate_position_x, plate_position_y, reference_z))

                # Orientation marker: a raised dot on the bottom-left corner of the plate.
                engine.add(phrase_scene, self._corner_marker(
                    plate_position_x - (final_plate_width / 2),
                    plate_position_y - (this_plate_height / 2),
                    plate_thickness,
                    resolution
                ))

                if rounded:
                    half_plate_height = this_plate_height / 2
                    border_plate = engine.create_plate(border_size, (this_plate_height - (border_size * 2)), plate_thickness)

                    engine.add(phrase_scene, engine.translate(engine.copy(border_cylinder),
                        border_cylinder_x_reference,
                        (plate_position_y + half_plate_height - border_size),
                        reference_z
                    ))
                    engine.add(phrase_scene, engine.translate(engine.copy(border_cylinder),
                        border_cylinder_x_reference + final_plate_width,
                        (plate_position_y + half_plate_height - border_size),
                        reference_z
                    ))
                    engine.add(phrase_scene, engine.translate(engine.copy(border_cylinder),
                        border_cylinder_x_reference,
                        (plate_position_y - half_plate_height + border_size),
                        reference_z
                    ))
                    engine.add(phrase_scene, engine.translate(engine.copy(border_cylinder),
                        border_cylinder_x_reference + final_plate_width,
                        (plate_position_y - half_plate_height + border_size),
                        reference_z
                    ))
                    engine.add(phrase_scene, engine.translate(engine.copy(border_plate),
                        (border_plate_x_reference - border_size),
                        plate_position_y,
                        reference_z
                    ))
                    engine.add(phrase_scene, engine.translate(engine.copy(border_plate),
                        (border_plate_x_reference + final_plate_width),
                        plate_position_y,
                        reference_z
                    ))

            for letter_index, letter in enumerate(phrase):
                if letter == "⠀":
                    continue

                letter_position_y = -(rules.dots_radius)
                letter_position_x = (letter_index * rules.cells_h_spacing) + rules.dots_radius
                letter_position_z = letter_reference_z
                if unique_plate:
                    letter_position_y -= (phrase_index * rules.cells_v_spacing)

                if text_alignment == "center":
                    letter_position_x += (plate_width - this_phrase_width) / 2
                elif text_alignment == "right":
                    letter_position_x += (plate_width - this_phrase_width)

                if letter not in char_cache:
                    char_cache[letter] = self._character_to_cell(letter, resolution, points_only)
                letter_in_3d = char_cache[letter]
                engine.add(phrase_scene, engine.translate(letter_in_3d, letter_position_x, letter_position_y, letter_position_z))

            phrase_mesh = engine.finalize(phrase_scene)
            phrase_position_z = phrase_index * (plate_thickness + rules.cells_v_spacing)
            if unique_plate:
                phrase_position_z = 0
            engine.add(scene, engine.translate(phrase_mesh, 0, 0, phrase_position_z))

        if unique_plate and not points_only:
            border_y_reference = (rules.cells_v_spacing + ((rules.cells_v_spacing - rules.cells_height) / 2))
            plate_height = (number_of_phrases * rules.cells_v_spacing) + rules.cells_v_spacing
            plate_position_x = plate_width / 2
            plate_position_y = border_y_reference - (plate_height / 2)

            final_plate_width = plate_width + rules.cells_v_spacing
            plate = engine.create_plate(final_plate_width, plate_height, plate_thickness)
            engine.add(scene, engine.translate(plate, plate_position_x, plate_position_y, reference_z))

            # Orientation marker: a raised dot on the bottom-left corner so the plate isn't
            # read/printed upside down.
            engine.add(scene, self._corner_marker(
                plate_position_x - (final_plate_width / 2),
                plate_position_y - (plate_height / 2),
                plate_thickness,
                resolution
            ))

            if rounded:
                border_plate = engine.create_plate(border_size, (plate_height - (border_size * 2)), plate_thickness)

                engine.add(scene, engine.translate(engine.copy(border_cylinder),
                    border_cylinder_x_reference,
                    (border_y_reference - border_size),
                    reference_z
                ))
                engine.add(scene, engine.translate(engine.copy(border_cylinder),
                    (border_cylinder_x_reference + final_plate_width),
                    (border_y_reference - border_size),
                    reference_z
                ))
                engine.add(scene, engine.translate(engine.copy(border_cylinder),
                    border_cylinder_x_reference,
                    (border_y_reference - plate_height + border_size),
                    reference_z
                ))
                engine.add(scene, engine.translate(engine.copy(border_cylinder),
                    (border_cylinder_x_reference + final_plate_width),
                    (border_y_reference - plate_height + border_size),
                    reference_z
                ))
                engine.add(scene, engine.translate(engine.copy(border_plate),
                    (border_plate_x_reference - border_size),
                    plate_position_y,
                    reference_z
                ))
                engine.add(scene, engine.translate(engine.copy(border_plate),
                    (border_plate_x_reference + final_plate_width),
                    plate_position_y,
                    reference_z
                ))

        if points_only:
            # Add a thin orientation bar below the lowest dots so the user knows which
            # side is "down" and doesn't glue the points upside down.
            combined = engine.finalize(scene)
            bounds = engine.bounds(combined)
            x_min, x_max, y_min = bounds[0], bounds[1], bounds[2]
            bar_width = x_max - x_min
            if bar_width > 0:
                bar_depth = 1.2
                bar_height = rules.dots_apparent_thickness
                bar_gap = 0.8
                bar = engine.create_plate(bar_width, bar_depth, bar_height)
                engine.add(scene, engine.translate(
                    bar,
                    (x_min + x_max) / 2,
                    y_min - bar_gap - (bar_depth / 2),
                    bar_height / 2
                ))

        final_mesh = engine.finalize(scene)
        return engine.translate(final_mesh, 0, 0, 0, 90)

    def _character_to_cell(self, character, resolution, points_only):
        code = BRAILLE_CODES[character]
        return self._build_cell(code, self._dimensions.dots_radius, self._dimensions.dots_spacing, resolution, points_only)

    def _build_cell(self, code, radius, spacing, resolution, points_only):
        engine = self._engine
        cell = engine.create_scene()

        # Every dot in a cell is the same shape, so build it once and reuse it.
        dot = engine.create_cap(radius, self._dimensions.dots_apparent_thickness, resolution) if points_only else engine.create_sphere(radius, resolution)

        dot_positions = [
            (0, 2 * spacing),
            (0, spacing),
            (0, 0),
            (spacing, 2 * spacing),
            (spacing, spacing),
            (spacing, 0),
        ]
        for index, (x, y) in enumerate(dot_positions):
            if code[index] == "1":
                engine.add(cell, engine.translate(dot, x, y, 0))

        return engine.finalize(cell)

    def _corner_marker(self, corner_x, corner_y, plate_thickness, resolution):
        engine = self._engine
        inset = 3.0
        marker_radius = 1.6
        marker = engine.create_cap(marker_radius, self._dimensions.dots_apparent_thickness, resolution)
        return engine.translate(marker, corner_x + inset, corner_y + inset, plate_thickness)
