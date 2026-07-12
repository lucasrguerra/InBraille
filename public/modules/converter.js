import { state } from './state.js';
import { getTranslation } from './i18n.js';

let dom = {};

export function initConverterDOM(elements) {
    dom = elements;
}

export function getAlphabet() {
    const checkedInput = document.querySelector('input[name="alphabet"]:checked');
    return checkedInput ? checkedInput.value : "North American";
}

export function switchConversionMode(mode) {
    state.conversion_mode = mode ? mode : state.conversion_mode;

    const text_to_braille_tab = dom.text_to_braille_tab;
    const braille_to_text_tab = dom.braille_to_text_tab;
    const input_label = dom.input_label;
    const input_textbox = dom.input_textbox;
    const output_label = dom.output_label;
    const output_textbox = dom.output_textbox;
    const warning = dom.warning;

    if (!text_to_braille_tab || !braille_to_text_tab || !input_label || !input_textbox || !output_label || !output_textbox || !warning) {
        return;
    }

    if (state.conversion_mode === "text-to-braille") {
        text_to_braille_tab.classList.add("tab-active");
        braille_to_text_tab.classList.remove("tab-active");

        input_label.innerHTML = `<i class="fas fa-pen-alt mr-1"></i> ${getTranslation("input_label_text_to_braille")}`;
        input_textbox.placeholder = getTranslation("input_placeholder_text_to_braille");
        output_label.innerHTML = `<span class="mr-1 font-bold">⠿</span> ${getTranslation("output_label_text_to_braille")}`;
        output_textbox.placeholder = getTranslation("output_placeholder_text_to_braille");

        warning.classList.add("hidden");
    } else {
        text_to_braille_tab.classList.remove("tab-active");
        braille_to_text_tab.classList.add("tab-active");

        input_label.innerHTML = `<span class="mr-1 font-bold">⠿</span> ${getTranslation("input_label_braille_to_text")}`;
        input_textbox.placeholder = getTranslation("input_placeholder_braille_to_text");
        output_label.innerHTML = `<i class="fas fa-text-width mr-1"></i> ${getTranslation("output_label_braille_to_text")}`;
        output_textbox.placeholder = getTranslation("output_placeholder_braille_to_text");

        if (getAlphabet() === "Brazilian") {
            warning.classList.remove("hidden");
        } else {
            warning.classList.add("hidden");
        }
    }

    const chineseTip = document.getElementById("chinese_input_tip_container");
    if (chineseTip) {
        if (getAlphabet() === "Chinese") {
            chineseTip.classList.remove("hidden");
        } else {
            chineseTip.classList.add("hidden");
        }
    }

    if (mode) {
        clearInput();
    }
}

export function clearInput() {
    if (dom.input_textbox) dom.input_textbox.value = "";
    if (dom.output_textbox) dom.output_textbox.value = "";
    updateCharCount();
}

export function updateCharCount() {
    if (!dom.char_count || !dom.input_textbox) return;
    const count = dom.input_textbox.value.length;
    if (state.page_language === "pt-BR") {
        dom.char_count.innerText = count + (count !== 1 ? " caracteres" : " caracter");
    } else if (state.page_language === "en") {
        dom.char_count.innerText = count + (count !== 1 ? " characters" : " character");
    } else if (state.page_language === "zh") {
        dom.char_count.innerText = count + " 个字符";
    }
}

export function copyOutput() {
    const output_textbox = dom.output_textbox;
    const copy_button = dom.copy_button;
    if (!output_textbox || !copy_button) return;
    
    if (!navigator.clipboard) {
        output_textbox.select();
        document.execCommand("copy");
    } else {
        const output = output_textbox.value;
        navigator.clipboard.writeText(output).then(() => {
            console.log(getTranslation("console_copy_success") || "Copied");
        }).catch(err => {
            console.error(getTranslation("console_copy_error") || "Error", err);
        });
    }

    const originalText = copy_button.innerText;
    const copyText = getTranslation("copy_button_feedback") || "Copied!";
    copy_button.innerHTML = `<i class="fas fa-check mr-1"></i> ${copyText}`;

    setTimeout(() => {
        copy_button.innerHTML = originalText;
    }, 2000);
}

export function saveOutput() {
    if (!dom.output_textbox) return;
    const text = dom.output_textbox.value;
    if (text.length === 0) { return; }

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `inbraille_output.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function adjustBrailleSize(braille) {
    const initial_string = String(braille).replaceAll("\n", "⠀");
    let adjusted_braille = "";
    let actual_phrase = "";

    const words = initial_string.split("⠀");
    const number_of_words = words.length;
    for (let index = 0; index < number_of_words; index++) {
        const word = words[index];
        const word_length = word.length;
        if (word_length > state.symbols_per_line) { return word_length; }

        if ((word_length + actual_phrase.length) > state.symbols_per_line) {
            adjusted_braille += actual_phrase.slice(0, -1) + "\n";
            actual_phrase = "";
        }

        actual_phrase += word + "⠀";
    }

    if (actual_phrase.length > 0) {
        adjusted_braille += actual_phrase.slice(0, -1);
    } else {
        adjusted_braille = adjusted_braille.slice(0, -1);
    }

    return adjusted_braille;
}

async function checkBrailleSize(braille) {
    const phrases = braille.split("\n");
    const number_of_phrases = phrases.length;
    for (let index = 0; index < number_of_phrases; index++) {
        const phrase = phrases[index];
        const phrase_length = phrase.length;
        if (phrase_length > state.symbols_per_line) {
            const adjust = confirm(getTranslation("confirm_line_exceeds"));

            if (adjust) {
                const adjusted = adjustBrailleSize(braille);
                if (isNaN(adjusted)) {
                    if (state.conversion_mode === "text-to-braille") {
                        const response = await axios.post("/api/decode", {
                            braille: adjusted,
                            alphabet: getAlphabet()
                        });
                        if (dom.input_textbox) {
                            dom.input_textbox.value = response.data.decoded;
                        }
                    }
                    alert(getTranslation("alert_auto_adjust_success"));
                } else {
                    alert(`${getTranslation("alert_word_exceeds_prefix")} ${adjusted}`);
                    return -1;
                }
                return adjusted;
            }
            return phrase_length;
        }
    }
    return phrases.join("\n");
}

export async function convert() {
    if (!dom.input_textbox || !dom.output_textbox) return;
    const text = dom.input_textbox.value;
    if (text.length === 0) { return; }

    const alphabet = getAlphabet();
    try {
        if (state.conversion_mode === "text-to-braille") {
            const response = await axios.post("/api/encode", {
                text: text,
                alphabet: alphabet
            });
            const braille = await checkBrailleSize(response.data.encoded);
            if (braille === -1) {
                // Alert already handled inside checkBrailleSize
            } else if (!isNaN(braille)) {
                dom.output_textbox.value = "";
                alert(`${getTranslation("alert_manual_correct_prefix")} ${braille}`);
            } else {
                dom.output_textbox.value = braille;
            }
        } else {
            const adjusted_braille = await checkBrailleSize(text);
            if (adjusted_braille === -1) {
                // Already handled
            } else if (!isNaN(adjusted_braille)) {
                dom.output_textbox.value = "";
                alert(`${getTranslation("alert_manual_correct_prefix")} ${adjusted_braille}`);
            } else {
                const response = await axios.post("/api/decode", {
                    braille: text,
                    alphabet: alphabet
                });
                dom.output_textbox.value = response.data.decoded;
            }
        }
    } catch (error) {
        console.error(error);
        alert(getTranslation("alert_general_error"));
    }
}
