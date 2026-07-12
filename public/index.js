import { state } from './modules/state.js';
import { setLanguage } from './modules/i18n.js';
import { initConverterDOM, switchConversionMode, updateCharCount, copyOutput, saveOutput, convert, clearInput } from './modules/converter.js';
import { initStlDOM, updateParameters, applyPointsOnlyState, updateInputs, generateSTL, downloadSTL, toggleAdvancedOptions } from './modules/stl.js';

document.addEventListener('DOMContentLoaded', function() {
    // Gather all DOM elements
    const elements = {
        text_to_braille_tab: document.querySelector("#text_to_braille_tab"),
        braille_to_text_tab: document.querySelector("#braille_to_text_tab"),
        warning: document.querySelector("#warning"),
        input_textbox: document.querySelector('#input_text'),
        input_label: document.querySelector('#input_label'),
        char_count: document.querySelector('#char_count'),
        output_textbox: document.querySelector('#output_text'),
        output_label: document.querySelector('#output_label'),
        copy_button: document.querySelector('#copy_button'),
        save_button: document.querySelector('#save_button'),
        convert_button: document.querySelector('#convert_button'),
        stl_button: document.querySelector('#stl_button'),
        stl_preview: document.querySelector('#stl_preview'),
        download_stl_button: document.querySelector('#download_stl_button'),
        advanced_options: document.querySelector("#advanced_options"),
        advanced_options_arrow: document.querySelector("#advanced_options_arrow"),
        advanced_options_toggle: document.querySelector("#advanced_options_toggle"),
        output_plate_width: document.querySelector("#plate_width"),
        input_resolution: document.querySelector("#input_resolution"),
        input_plate_thickness: document.querySelector("#input_plate_thickness"),
        input_separate_plates: document.querySelector("#input_separate_plates"),
        input_symbols_per_line: document.querySelector("#input_symbols_per_line"),
        select_text_alignment: document.querySelector("#select_text_alignment"),
        input_rounded: document.querySelector("#input_rounded"),
        input_points_only: document.querySelector("#input_points_only")
    };

    // Initialize modules with DOM references
    initConverterDOM(elements);
    initStlDOM(elements);

    // Initial value setup
    if (elements.input_resolution) elements.input_resolution.value = state.resolution;
    if (elements.input_plate_thickness) elements.input_plate_thickness.value = state.plate_thickness;
    if (elements.input_separate_plates) elements.input_separate_plates.checked = !state.unique_plate;
    if (elements.input_symbols_per_line) elements.input_symbols_per_line.value = state.symbols_per_line;
    if (elements.select_text_alignment) elements.select_text_alignment.value = state.text_alignment;
    if (elements.input_rounded) elements.input_rounded.checked = state.rounded;
    if (elements.input_points_only) elements.input_points_only.checked = state.points_only;
    if (elements.output_plate_width) elements.output_plate_width.innerHTML = state.plate_width.toFixed(1);
    applyPointsOnlyState();

    // Event listeners registration
    if (elements.text_to_braille_tab) {
        elements.text_to_braille_tab.addEventListener("click", () => switchConversionMode("text-to-braille"));
    }
    if (elements.braille_to_text_tab) {
        elements.braille_to_text_tab.addEventListener("click", () => switchConversionMode("braille-to-text"));
    }
    if (elements.input_textbox) {
        elements.input_textbox.addEventListener("input", updateCharCount);
    }
    if (elements.copy_button) {
        elements.copy_button.addEventListener("click", copyOutput);
    }
    if (elements.save_button) {
        elements.save_button.addEventListener("click", saveOutput);
    }
    if (elements.convert_button) {
        elements.convert_button.addEventListener("click", convert);
    }
    if (elements.stl_button) {
        elements.stl_button.addEventListener("click", generateSTL);
    }
    if (elements.download_stl_button) {
        elements.download_stl_button.addEventListener("click", downloadSTL);
    }
    if (elements.advanced_options_toggle) {
        elements.advanced_options_toggle.addEventListener("click", toggleAdvancedOptions);
    }

    if (elements.input_resolution) {
        elements.input_resolution.addEventListener("input", updateParameters);
    }
    if (elements.input_plate_thickness) {
        elements.input_plate_thickness.addEventListener("input", updateParameters);
    }
    if (elements.input_separate_plates) {
        elements.input_separate_plates.addEventListener("input", updateParameters);
    }
    if (elements.input_symbols_per_line) {
        elements.input_symbols_per_line.addEventListener("input", updateParameters);
        elements.input_symbols_per_line.addEventListener("change", convert);
    }
    if (elements.select_text_alignment) {
        elements.select_text_alignment.addEventListener("input", updateParameters);
    }
    if (elements.input_rounded) {
        elements.input_rounded.addEventListener("input", updateParameters);
    }
    if (elements.input_points_only) {
        elements.input_points_only.addEventListener("input", () => {
            updateParameters();
            applyPointsOnlyState();
        });
    }

    if (elements.input_resolution) elements.input_resolution.addEventListener("blur", updateInputs);
    if (elements.input_plate_thickness) elements.input_plate_thickness.addEventListener("blur", updateInputs);
    if (elements.input_separate_plates) elements.input_separate_plates.addEventListener("blur", updateInputs);
    if (elements.input_symbols_per_line) {
        elements.input_symbols_per_line.addEventListener("blur", () => {
            updateInputs();
            convert();
        });
    }
    if (elements.select_text_alignment) elements.select_text_alignment.addEventListener("blur", updateInputs);
    if (elements.input_rounded) elements.input_rounded.addEventListener("blur", updateInputs);

    // Helper to switch language and update dependent components
    function changeLanguage(lang, callback) {
        setLanguage(lang, () => {
            switchConversionMode();
            updateInputs();
            if (callback) callback();
        });
    }

    // Language switcher click handlers
    document.querySelectorAll("#lang_dropdown button[data-lang]").forEach(button => {
        button.addEventListener("click", (e) => {
            const selectedLang = e.currentTarget.getAttribute("data-lang");
            
            changeLanguage(selectedLang, () => {
                let newPath = "/";
                if (selectedLang === "en") newPath = "/en";
                else if (selectedLang === "zh") newPath = "/zh";
                
                window.history.pushState(null, "", newPath);
            });
        });
    });

    // Clear button listener
    const clearBtn = document.querySelector("#clear_button");
    if (clearBtn) {
        clearBtn.addEventListener("click", clearInput);
    }

    // Alphabet radio listener
    document.querySelectorAll('input[name="alphabet"]').forEach(radio => {
        radio.addEventListener("change", () => switchConversionMode());
    });

    // Determine and set initial language and default alphabet
    const path = window.location.pathname;
    let initialLang = "pt-BR";
    if (path.startsWith("/en")) {
        initialLang = "en";
        const radio = document.getElementById("north-american");
        if (radio) radio.checked = true;
    } else if (path.startsWith("/zh")) {
        initialLang = "zh";
        const radio = document.getElementById("chinese");
        if (radio) radio.checked = true;
    } else {
        const radio = document.getElementById("brazilian");
        if (radio) radio.checked = true;
    }
    changeLanguage(initialLang);
});