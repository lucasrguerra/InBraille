import { state, updatePlateWidth } from './state.js';
import { getTranslation } from './i18n.js';
import { showToast, highlightInput } from './ui.js';
import { convert } from './converter.js';

let dom = {};

export function initStlDOM(elements) {
    dom = elements;
}

export function updateParameters() {
    if (!dom.input_resolution || !dom.input_plate_thickness || !dom.input_separate_plates || !dom.input_symbols_per_line || !dom.select_text_alignment || !dom.input_rounded || !dom.input_points_only) {
        return;
    }
    state.resolution = parseInt(dom.input_resolution.value) || 20;
    state.plate_thickness = parseInt(dom.input_plate_thickness.value) || 3;
    state.unique_plate = !dom.input_separate_plates.checked;
    state.symbols_per_line = parseInt(dom.input_symbols_per_line.value) || 22;
    state.text_alignment = dom.select_text_alignment.value || "center";
    state.rounded = dom.input_rounded.checked;
    state.points_only = dom.input_points_only.checked;
    updatePlateWidth();
}

export function applyPointsOnlyState() {
    if (!dom.input_separate_plates || !dom.input_rounded || !dom.input_plate_thickness) return;
    const disabled_inputs = [dom.input_separate_plates, dom.input_rounded, dom.input_plate_thickness];
    disabled_inputs.forEach((input) => {
        input.disabled = state.points_only;
        const card = input.closest(".bg-white");
        if (card) {
            card.classList.toggle("opacity-50", state.points_only);
            card.classList.toggle("pointer-events-none", state.points_only);
        }
    });
}

export function updateInputs() {
    if (!dom.input_resolution || !dom.input_plate_thickness || !dom.input_separate_plates || !dom.input_symbols_per_line || !dom.select_text_alignment || !dom.input_rounded || !dom.input_points_only || !dom.output_plate_width) {
        return;
    }

    if (state.symbols_per_line < 8) { state.symbols_per_line = 8; }
    if (state.symbols_per_line > 50) { state.symbols_per_line = 50; }

    if (state.plate_thickness < 2) { state.plate_thickness = 2; }
    if (state.plate_thickness > 100) { state.plate_thickness = 100; }

    if (state.resolution < 15) { state.resolution = 15; }
    if (state.resolution > 50) { state.resolution = 50; }

    dom.input_resolution.value = state.resolution;
    dom.input_plate_thickness.value = state.plate_thickness;
    dom.input_separate_plates.checked = !state.unique_plate;
    dom.input_symbols_per_line.value = state.symbols_per_line;
    dom.select_text_alignment.value = state.text_alignment;
    dom.input_rounded.checked = state.rounded;
    dom.input_points_only.checked = state.points_only;
    dom.output_plate_width.innerHTML = state.plate_width.toFixed(1);
}

export async function generateSTL() {
    const input_textbox = dom.input_textbox;
    const output_textbox = dom.output_textbox;
    const stl_button = dom.stl_button;
    if (!input_textbox || !output_textbox || !stl_button) return;

    if (state.conversion_mode === "braille-to-text") {
        if (input_textbox.value.trim().length === 0) {
            showToast(getTranslation("toast_enter_braille"), "warning");
            highlightInput(input_textbox);
            return;
        }
    } else if (output_textbox.value.trim().length === 0) {
        if (input_textbox.value.trim().length === 0) {
            showToast(getTranslation("toast_enter_text"), "warning");
            highlightInput(input_textbox);
            return;
        }

        showToast(getTranslation("toast_converting"), "info");
        await convert();
        if (output_textbox.value.trim().length === 0) {
            return;
        }
    }

    let braille = output_textbox.value;
    if (state.conversion_mode === "braille-to-text") {
        braille = input_textbox.value;
    }
    if (braille.length === 0) { return; }

    stl_button.disabled = true;
    const genText = getTranslation("generating_loader") || "Generating...";
    stl_button.innerHTML = `<i class="fas fa-spinner fa-spin mr-1"></i>${genText}`;

    try {
        const response = await axios.post("/api/to-stl", {
            braille: braille,
            resolution: state.resolution,
            plate_thickness: state.plate_thickness,
            unique_plate: state.unique_plate,
            symbols_per_line: state.symbols_per_line,
            text_alignment: state.text_alignment,
            rounded: state.rounded,
            points_only: state.points_only
        }, { responseType: 'arraybuffer' });

        state.last_stl_blob = new Blob([response.data], { type: "model/stl" });

        if (dom.stl_preview) {
            dom.stl_preview.classList.remove("hidden");
        }
        if (typeof window.renderSTLPreview === "function") {
            window.renderSTLPreview(response.data.slice(0));
        }
        if (dom.stl_preview) {
            dom.stl_preview.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
    } catch (error) {
        console.error(error);
        alert(getTranslation("alert_stl_error"));
    } finally {
        stl_button.disabled = false;
        const genDoneText = getTranslation("stl_button_default") || "Generate & Preview STL";
        stl_button.innerHTML = `<i class="fas fa-cube mr-2"></i>${genDoneText}`;
    }
}

export function downloadSTL() {
    if (!state.last_stl_blob) { return; }

    const url = window.URL.createObjectURL(state.last_stl_blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'output.stl');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

export function toggleAdvancedOptions() {
    if (dom.advanced_options && dom.advanced_options_arrow) {
        dom.advanced_options.classList.toggle("hidden");
        dom.advanced_options_arrow.classList.toggle("rotate-180");
    }
}
