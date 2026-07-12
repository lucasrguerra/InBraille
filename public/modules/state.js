export const state = {
    page_language: "pt-BR",
    conversion_mode: "text-to-braille",
    resolution: 20,
    plate_thickness: 2,
    unique_plate: true,
    symbols_per_line: 22,
    text_alignment: "center",
    rounded: false,
    points_only: false,
    plate_width: 143.3, // calculated default
    last_stl_blob: null
};

export function calculatePlateWidth() {
    return ((state.symbols_per_line - 1) * 6.6) + 4.7;
}

export function updatePlateWidth() {
    state.plate_width = calculatePlateWidth();
}
