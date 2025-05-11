"use strict";

let page_language = "pt-BR";
let conversion_mode = "text-to-braille";
let resolution = 20;
let plate_thickness = 2;
let unique_plate = true;
let unique_width = true;
let text_alignment = "center";
let rounded = false;

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

let input_resolution = null;
let input_plate_thickness = null;
let input_unique_plate = null;
let input_unique_width = null;
let select_text_alignment = null;
let input_rounded = null;

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

async function convert() {
    const text = input_textbox.value;
    if (text.length === 0) { return; }

    const alphabet = getAlphabet();
    try {
        if (conversion_mode === "text-to-braille") {
            await axios.post("/api/encode", {
                text: text,
                alphabet: alphabet
            }).then((response) => {
                const braille = response.data.encoded;
                output_textbox.innerHTML = braille;
            });
        } else {
            await axios.post("/api/decode", {
                braille: text,
                alphabet: alphabet
            }).then((response) => {
                const decodedText = response.data.decoded;
                output_textbox.innerHTML = decodedText;
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
            unique_width: unique_width,
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
    resolution = input_resolution.value;
    plate_thickness = input_plate_thickness.value;
    unique_plate = input_unique_plate.checked;
    unique_width = input_unique_width.checked;
    text_alignment = select_text_alignment.value;
    rounded = input_rounded.checked;

    if (unique_plate) {
        unique_width = true;
        input_unique_width.checked = true;
        input_unique_width.disabled = true;
    } else {
        input_unique_width.disabled = false;
    }

    if (!unique_width && !unique_plate) {
        text_alignment = "center";
        select_text_alignment.value = "center";
        select_text_alignment.disabled = true;
    } else {
        select_text_alignment.disabled = false;
    }
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

    input_resolution = document.querySelector("#input_resolution");
    input_plate_thickness = document.querySelector("#input_plate_thickness");
    input_unique_plate = document.querySelector("#input_unique_plate");
    input_unique_width = document.querySelector("#input_unique_width");
    select_text_alignment = document.querySelector("#select_text_alignment");
    input_rounded = document.querySelector("#input_rounded");

    input_resolution.value = resolution;
    input_plate_thickness.value = plate_thickness;
    input_unique_plate.checked = unique_plate;
    input_unique_width.checked = unique_width;
    select_text_alignment.value = text_alignment;
    input_rounded.checked = rounded;

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
    input_unique_plate.addEventListener("input", updateParameters);
    input_unique_width.addEventListener("input", updateParameters);
    select_text_alignment.addEventListener("input", updateParameters);
    input_rounded.addEventListener("input", updateParameters);
});