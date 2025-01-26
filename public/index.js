var alphabet = "North American";
var radius = 0.7;
var spacing = 2.2;
var kerning = 2.8;
var subdivisions = 2;
var thickness = 1;
var unique_plate = false;
var unique_width = false;
var text_alignment = "left";
var rounded = false;

async function encodeTextToBraille(event) {
    const text = event.target.value;
    if (text === "") {
        input_braille.value = "";
        return;
    }

    try {
        await axios.post("/api/encode", {
            text: text,
            alphabet: alphabet
        }).then((response) => {
            input_braille.value = response.data.encoded;
        });
    } catch (error) {
        console.error(error);
        alert("An error occurred while encoding the text to braille.");
    }
}

async function decodeBrailleToText(event) {
    const braille = event.target.value;
    if (braille === "") {
        input_text.value = "";
        return;
    }

    try {
        await axios.post("/api/decode", {
            braille: braille,
            alphabet: alphabet
        }).then((response) => {
            input_text.value = response.data.decoded;
        });
    } catch (error) {
        console.error(error);
        alert("An error occurred while decoding the braille to text.");
    }
}

async function downloadSTL(event) {
    event.preventDefault();

    event.target.disabled = true;
    event.target.textContent = "Downloading...";

    const braille = input_braille.value;
    if (braille === "") {
        alert("Please enter some braille text to download the STL file.");
        return;
    }

    try {
        await axios.post("/api/to-stl", {
            braille: braille,
            radius: radius,
            spacing: spacing,
            kerning: kerning,
            subdivisions: subdivisions,
            thickness: thickness,
            unique_plate: unique_plate,
            unique_width: unique_width,
            text_alignment: text_alignment,
            rounded: rounded
        },{ responseType: 'blob' }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'output.stl');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    } catch (error) {
        console.error(error);
        alert("An error occurred while downloading the STL file.");
    }

    event.target.disabled = false;
    event.target.textContent = "Convert to STL file";
}

document.addEventListener('DOMContentLoaded', function() {
    const select_alphabet = document.querySelector("#select_alphabet");
    const input_text = document.querySelector("#input_text");
    const input_braille = document.querySelector("#input_braille");
    const stl_button = document.querySelector("#stl_button");
    const input_radius = document.querySelector("#input_radius");
    const input_spacing = document.querySelector("#input_spacing");
    const input_kerning = document.querySelector("#input_kerning");
    const input_subdivisions = document.querySelector("#input_subdivisions");
    const input_thickness = document.querySelector("#input_thickness");
    const input_unique_plate = document.querySelector("#input_unique_plate");
    const input_unique_width = document.querySelector("#input_unique_width");
    const select_text_alignment = document.querySelector("#select_text_alignment");
    const input_rounded = document.querySelector("#input_rounded");
    const warning = document.querySelector("#warning");

    input_text.addEventListener("input", encodeTextToBraille);
    input_braille.addEventListener("input", decodeBrailleToText);
    stl_button.addEventListener("click", downloadSTL);

    select_alphabet.value = alphabet;
    select_alphabet.addEventListener("input", function(event) {
        alphabet = event.target.value;
        input_text.dispatchEvent(new Event("input"));

        try {
            if (alphabet === "Brazilian") {
                warning.classList.replace("hidden", "block");
            } else {
                warning.classList.replace("block", "hidden");
            }
        } catch (error) {}
    });

    input_radius.value = radius;
    input_radius.addEventListener("input", function(event) {
        radius = parseFloat(event.target.value);
    });

    input_spacing.value = spacing;
    input_spacing.addEventListener("input", function(event) {
        spacing = parseFloat(event.target.value);
    });

    input_kerning.value = kerning;
    input_kerning.addEventListener("input", function(event) {
        kerning = parseFloat(event.target.value);
    });

    input_subdivisions.value = subdivisions;
    input_subdivisions.addEventListener("input", function(event) {
        subdivisions = parseInt(event.target.value);

        if (subdivisions < 1) {
            subdivisions = 1;
        } else if (subdivisions > 4) {
            subdivisions = 4;
        }
    });

    input_thickness.value = thickness;
    input_thickness.addEventListener("input", function(event) {
        thickness = parseFloat(event.target.value);
    });

    input_unique_plate.checked = unique_plate;
    input_unique_plate.addEventListener("input", function(event) {
        unique_plate = event.target.checked;

        if (unique_plate && !unique_width) {
            input_rounded.checked = false;
            input_rounded.disabled = true;
            rounded = false;
        } else {
            input_rounded.disabled = false;
        }
    });

    input_unique_width.checked = unique_width;
    input_unique_width.addEventListener("input", function(event) {
        unique_width = event.target.checked;

        if (unique_plate && !unique_width) {
            input_rounded.checked = false;
            input_rounded.disabled = true;
            rounded = false;
        } else {
            input_rounded.disabled = false;
        }
    });

    select_text_alignment.value = text_alignment;
    select_text_alignment.addEventListener("input", function(event) {
        text_alignment = event.target.value;
    });

    input_rounded.checked = rounded;
    input_rounded.addEventListener("input", function(event) {
        rounded = event.target.checked;
    });
});