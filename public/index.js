var alphabet = "";
var resolution = 20;
var plate_thickness = 2;
var unique_plate = true;
var unique_width = true;
var text_alignment = "center";
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
        alert("Tente Novamente\nTry Again");
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
        alert("Tente Novamente\nTry Again");
    }
}

async function downloadSTL(event) {
    event.preventDefault();
    
    const braille = input_braille.value;
    if (braille === "") {
        alert("Tente Novamente\nTry Again");
        return;
    }
    
    const button_text = event.target.textContent;
    event.target.disabled = true;
    event.target.textContent = "Downloading...";
    try {
        await axios.post("/api/to-stl", {
            braille: braille,
            resolution: resolution,
            plate_thickness: plate_thickness,
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
        alert("Tente Novamente\nTry Again");
    }

    event.target.disabled = false;
    event.target.textContent = button_text;
}

document.addEventListener('DOMContentLoaded', function() {
    const select_alphabet = document.querySelector("#select_alphabet");
    const input_text = document.querySelector("#input_text");
    const input_braille = document.querySelector("#input_braille");
    const stl_button = document.querySelector("#stl_button");
    const input_resolution = document.querySelector("#input_resolution");
    const input_plate_thickness = document.querySelector("#input_plate_thickness");
    const input_unique_plate = document.querySelector("#input_unique_plate");
    const input_unique_width = document.querySelector("#input_unique_width");
    const select_text_alignment = document.querySelector("#select_text_alignment");
    const input_rounded = document.querySelector("#input_rounded");
    const warning = document.querySelector("#warning");

    input_text.addEventListener("input", encodeTextToBraille);
    input_braille.addEventListener("input", decodeBrailleToText);
    stl_button.addEventListener("click", downloadSTL);

    alphabet = select_alphabet.value;
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

    input_resolution.value = resolution;
    input_resolution.addEventListener("input", function(event) {
        resolution = parseInt(event.target.value);

        if (resolution < 2) {
            resolution = 2;
        } else if (resolution > 150) {
            resolution = 150;
        }
    });

    input_plate_thickness.value = plate_thickness;
    input_plate_thickness.addEventListener("input", function(event) {
        plate_thickness = parseFloat(event.target.value);

        if (plate_thickness < 2) {
            plate_thickness = 2;
        } else if (plate_thickness > 100) {
            plate_thickness = 100;
        }
    });

    input_unique_plate.checked = unique_plate;
    input_unique_plate.addEventListener("input", function(event) {
        unique_plate = event.target.checked;
        select_text_alignment.disabled = (!unique_plate && !unique_width);

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
        select_text_alignment.disabled = (!unique_plate && !unique_width);

        if (unique_plate && !unique_width) {
            input_rounded.checked = false;
            input_rounded.disabled = true;
            rounded = false;
        } else {
            input_rounded.disabled = false;
        }
    });

    select_text_alignment.value = text_alignment;
    select_text_alignment.disabled = !unique_plate;
    select_text_alignment.addEventListener("input", function(event) {
        text_alignment = event.target.value;
    });

    input_rounded.checked = rounded;
    input_rounded.addEventListener("input", function(event) {
        rounded = event.target.checked;
    });
});