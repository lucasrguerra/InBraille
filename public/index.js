"use strict";

let page_language = "pt-BR";
let conversion_mode = "text-to-braille";
let resolution = 20;
let plate_thickness = 2;
let unique_plate = true;
let symbols_per_line = 22;
let text_alignment = "center";
let rounded = false;
let plate_width = calculatePlateWidth();

let text_to_braille_tab = null;
let braille_to_text_tab = null;
let warning = null;
let input_textbox = null;
let input_label = null;
let char_count = null;
let output_textbox = null;
let output_label = null;
let copy_button = null;
let save_button = null;
let convert_button = null;
let stl_button = null;
let advanced_options = null;
let advanced_options_arrow = null;
let advanced_options_toggle = null;
let output_plate_width = null;

let input_resolution = null;
let input_plate_thickness = null;
let input_separate_plates = null;
let input_symbols_per_line = null;
let select_text_alignment = null;
let input_rounded = null;

function calculatePlateWidth() {
    return ((symbols_per_line - 1) * 6.6) + 4.7;
}

function getAlphabet() {
    const alphabet = document.querySelector('input[name="alphabet"]:checked').value;
    return alphabet;
}

function switchConversionMode(mode) {
    conversion_mode = mode ? mode : conversion_mode;

    if (conversion_mode === "text-to-braille") {
        text_to_braille_tab.classList.add("tab-active");
        braille_to_text_tab.classList.remove("tab-active");

        if (page_language === "pt-BR") {
            input_label.innerHTML = `<i class="fas fa-pen-alt mr-1"></i> Digite seu texto`;
            input_textbox.placeholder = "Digite o texto que deseja converter para Braille...";
            output_label.innerHTML = `<span class="mr-1 font-bold">⠿</span> Resultado em Braille`;
            output_textbox.innerHTML = "O resultado em Braille aparecerá aqui...";
        } else if (page_language === "en") {
            input_label.innerHTML = `<i class="fas fa-pen-alt mr-1"></i> Type your text`;
            input_textbox.placeholder = "Type the text you want to convert to Braille...";
            output_label.innerHTML = `<span class="mr-1 font-bold">⠿</span> Result in Braille`;
            output_textbox.innerHTML = "The result in Braille will appear here...";
        }

        warning.classList.add("hidden");
    } else {
        text_to_braille_tab.classList.remove("tab-active");
        braille_to_text_tab.classList.add("tab-active");

        if (page_language === "pt-BR") {
            input_label.innerHTML = `<span class="mr-1 font-bold">⠿</span> Digite em Braille`;
            input_textbox.placeholder = "Digite o texto em Braille que deseja converter...";
            output_label.innerHTML = `<i class="fas fa-text-width mr-1"></i> Resultado em Texto`;
            output_textbox.innerHTML = "O resultado em texto aparecerá aqui...";
        } else if (page_language === "en") {
            input_label.innerHTML = `<span class="mr-1 font-bold">⠿</span> Type in Braille`;
            input_textbox.placeholder = "Type the text in Braille you want to convert...";
            output_label.innerHTML = `<i class="fas fa-text-width mr-1"></i> Result in Text`;
            output_textbox.innerHTML = "The result in text will appear here...";
        }

        if (getAlphabet() === "Brazilian") {
            warning.classList.remove("hidden");
        } else {
            warning.classList.add("hidden");
        }
    }

    clearInput();
}

function clearInput() {
    input_textbox.value = "";
    output_textbox.innerText = "";
    updateCharCount();
}

function updateCharCount() {
    const count = input_textbox.value.length;
    if (page_language === "pt-BR") {
        char_count.innerText = count + " caracter";
        if (count !== 1) {
            char_count.innerText += "es";
        }
    } else if (page_language === "en") {
        char_count.innerText = count + " character";
        if (count !== 1) {
            char_count.innerText += "s";
        }
    }
}

function toggleAdvancedOptions() {
    advanced_options.classList.toggle("hidden");
    advanced_options_arrow.classList.toggle("rotate-180");
}

function copyOutput() {
    if (!navigator.clipboard) {
        output_textbox.select();
        document.execCommand("copy");
        
    } else {
        const output = output_textbox.value;
        navigator.clipboard.writeText(output).then(() => {
            console.log("Texto copiado para a área de transferência");
        }).catch(err => {
            console.error("Erro ao copiar o texto: ", err);
        });
    }

    const originalText = copy_button.innerText;
    if (page_language === "pt-BR") {
        copy_button.innerHTML = `<i class="fas fa-check mr-1"></i> Copiado!`;
    } else if (page_language === "en") {
        copy_button.innerHTML = `<i class="fas fa-check mr-1"></i> Copied!`;
    }

    setTimeout(() => {
        copy_button.innerHTML = originalText;
    }, 2000);
}

function saveOutput() {
    const text = output_textbox.value;
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
        if (word_length > symbols_per_line) { return word_length; }

        if ((word_length + actual_phrase.length) > symbols_per_line) {
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
        if (phrase_length > symbols_per_line) {
            
            let adjust = false;
            if (page_language === "pt-BR") {
                adjust = confirm(`Uma das linhas ultrapassa o limite de símbolos por linha.\nVocê quer que o programa tente ajustar automaticamente?`);
            } else if (page_language === "en") {
                adjust = confirm(`One of the lines exceeds the symbol limit per line.\nDo you want the program to try to adjust it automatically?`);
            }

            if (adjust) {
                const adjusted = adjustBrailleSize(braille);
                if (!isNaN(adjusted)) {
                    if (page_language === "pt-BR") {
                        alert(`Uma das palavras ultrapassa o limite de símbolos por linha.\nNas opções avançadas, ajuste a quantidade de símbolos por linha para no mínimo ${adjusted}`);
                    } else if (page_language === "en") {
                        alert(`One of the words exceeds the symbol limit per line.\nIn the advanced options, adjust the number of symbols per line to at least ${adjusted}`);
                    }

                    return -1;
                }  else {
                    if (conversion_mode === "text-to-braille") {
                        await axios.post("/api/decode", {
                            braille: adjusted,
                            alphabet: getAlphabet()
                        }).then((response) => {
                            const decodedText = response.data.decoded;
                            input_textbox.value = decodedText;
                        });
                    }

                    if (page_language === "pt-BR") {
                        alert(`O programa conseguiu ajustar automaticamente a linha.\n`);
                    } else if (page_language === "en") {
                        alert(`The program was able to automatically adjust the line.\n`);
                    }
                }

                return adjusted;
            }

            return phrase_length;
        }
    }
    return phrases.join("\n");
}

async function convert() {
    const text = input_textbox.value;
    if (text.length === 0) { return; }

    const alphabet = getAlphabet();
    try {
        if (conversion_mode === "text-to-braille") {
            await axios.post("/api/encode", {
                text: text,
                alphabet: alphabet
            }).then(async (response) => {
                const braille = await checkBrailleSize(response.data.encoded);
                if (!isNaN(braille) && braille !== -1) {
                    output_textbox.value = "";

                    if (page_language === "pt-BR") {
                        alert(`Corrija manualmente ou, ajuste a quantidade de símbolos por linha para no mínimo ${braille} nas opções avançadas`);
                    } else if (page_language === "en") {
                        alert(`Manually correct or adjust the number of symbols per line to at least ${braille} in the advanced options`);
                    }
                } else if (braille !== -1) {
                    output_textbox.value = braille;
                }
            });
        } else {
            const adjusted_braille = await checkBrailleSize(text);
            if (!isNaN(adjusted_braille)) {
                output_textbox.value = "";

                if (adjusted_braille !== -1) {
                    if (page_language === "pt-BR") {
                        alert(`Corrija manualmente ou, ajuste a quantidade de símbolos por linha para no mínimo ${adjusted_braille} nas opções avançadas`);
                    } else if (page_language === "en") {
                        alert(`Manually correct or adjust the number of symbols per line to at least ${adjusted_braille} in the advanced options`);
                    }
                }

                return;
            }

            await axios.post("/api/decode", {
                braille: text,
                alphabet: alphabet
            }).then((response) => {
                const decodedText = response.data.decoded;
                output_textbox.value = decodedText;
            });
        }
    } catch (error) {
        console.error(error);
        alert("Tente Novamente\nTry Again");
    }
}

function generateSTL() {
    let braille = output_textbox.value;
    if (conversion_mode === "braille-to-text") {
        braille = input_textbox.value;
    }
    if (braille.length === 0) { return; }

    stl_button.disabled = true;
    stl_button.innerHTML = `<i class="fas fa-spinner fa-spin mr-1"></i>Gerando...`;
    try {
        axios.post("/api/to-stl", {
            braille: braille,
            resolution: resolution,
            plate_thickness: plate_thickness,
            unique_plate: unique_plate,
            symbols_per_line: symbols_per_line,
            text_alignment: text_alignment,
            rounded: rounded
        }, { responseType: 'blob' }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'output.stl');
            document.body.appendChild(link);
            link.click();
        });
    } catch (error) {
        console.error(error);
        if (page_language === "pt-BR") {
            alert("Erro ao gerar o arquivo STL. Tente novamente.");
        } else if (page_language === "en") {
            alert("Error generating STL file. Please try again.");
        }
    } finally {
        stl_button.disabled = false;
        if (page_language === "pt-BR") {
            stl_button.innerHTML = `<i class="fas fa-cube mr-2"></i>Gerar Arquivo STL`;
        } else if (page_language === "en") {
            stl_button.innerHTML = `<i class="fas fa-cube mr-2"></i>Generate STL File`;
        }
    }
}

function updateParameters() {
    resolution = parseInt(input_resolution.value);
    plate_thickness = parseInt(input_plate_thickness.value);
    unique_plate = !input_separate_plates.checked;
    symbols_per_line = parseInt(input_symbols_per_line.value);
    text_alignment = select_text_alignment.value;
    rounded = input_rounded.checked;
    plate_width = calculatePlateWidth();
}

function updateInputs() {
    if (symbols_per_line < 8) { symbols_per_line = 8; }
    if (symbols_per_line > 50) { symbols_per_line = 50; }

    if (plate_thickness < 2) { plate_thickness = 2; }
    if (plate_thickness > 100) { plate_thickness = 100; }

    if (resolution < 15) { resolution = 15; }
    if (resolution > 50) { resolution = 50; }

    input_resolution.value = resolution;
    input_plate_thickness.value = plate_thickness;
    input_separate_plates.checked = !unique_plate;
    input_symbols_per_line.value = symbols_per_line;
    select_text_alignment.value = text_alignment;
    input_rounded.checked = rounded;
    output_plate_width.innerHTML = plate_width.toFixed(1);
}

document.addEventListener('DOMContentLoaded', function() {
    page_language = document.documentElement.lang;

    text_to_braille_tab = document.querySelector("#text_to_braille_tab");
    braille_to_text_tab = document.querySelector("#braille_to_text_tab");
    warning = document.querySelector("#warning");
    input_textbox = document.querySelector('#input_text');
    input_label = document.querySelector('#input_label');
    char_count = document.querySelector('#char_count');
    output_textbox = document.querySelector('#output_text');
    output_label = document.querySelector('#output_label');
    copy_button = document.querySelector('#copy_button');
    save_button = document.querySelector('#save_button');
    convert_button = document.querySelector('#convert_button');
    stl_button = document.querySelector('#stl_button');
    advanced_options = document.querySelector("#advanced_options");
    advanced_options_arrow = document.querySelector("#advanced_options_arrow");
    advanced_options_toggle = document.querySelector("#advanced_options_toggle");
    output_plate_width = document.querySelector("#plate_width");

    input_resolution = document.querySelector("#input_resolution");
    input_plate_thickness = document.querySelector("#input_plate_thickness");
    input_separate_plates = document.querySelector("#input_separate_plates");
    input_symbols_per_line = document.querySelector("#input_symbols_per_line");
    select_text_alignment = document.querySelector("#select_text_alignment");
    input_rounded = document.querySelector("#input_rounded");

    input_resolution.value = resolution;
    input_plate_thickness.value = plate_thickness;
    input_separate_plates.checked = !unique_plate;
    input_symbols_per_line.value = symbols_per_line;
    select_text_alignment.value = text_alignment;
    input_rounded.checked = rounded;
    output_plate_width.innerHTML = plate_width.toFixed(1);

    text_to_braille_tab.addEventListener("click", () => switchConversionMode("text-to-braille"));
    braille_to_text_tab.addEventListener("click", () => switchConversionMode("braille-to-text"));
    input_textbox.addEventListener("input", updateCharCount);
    copy_button.addEventListener("click", copyOutput);
    save_button.addEventListener("click", saveOutput);
    convert_button.addEventListener("click", convert);
    stl_button.addEventListener("click", generateSTL);
    advanced_options_toggle.addEventListener("click", toggleAdvancedOptions);

    input_resolution.addEventListener("input", updateParameters);
    input_plate_thickness.addEventListener("input",updateParameters);
    input_separate_plates.addEventListener("input", updateParameters);
    input_symbols_per_line.addEventListener("input", updateParameters);
    select_text_alignment.addEventListener("input", updateParameters);
    input_rounded.addEventListener("input", updateParameters);

    input_resolution.addEventListener("blur", updateInputs);
    input_plate_thickness.addEventListener("blur", updateInputs);
    input_separate_plates.addEventListener("blur", updateInputs);
    input_symbols_per_line.addEventListener("blur", updateInputs);
    select_text_alignment.addEventListener("blur", updateInputs);
    input_rounded.addEventListener("blur", updateInputs);
});