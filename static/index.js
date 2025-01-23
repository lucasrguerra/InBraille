var size = 2;
var spacing = 5;
var kerning = 2.5;
var subdivisions = 2;
var surface_depth = 2;
var unique_surface = false;
var unique_width = false;
var text_alignment = "left";

async function encodeTextToBraille(event) {
    const text = event.target.value;
    if (text === "") {
        input_braille.value = "";
        return;
    }

    try {
        await axios.post("/api/encode", { text: text }).then((response) => {
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
        await axios.post("/api/decode", { braille: braille }).then((response) => {
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
            size: size,
            spacing: spacing,
            kerning: kerning,
            subdivisions: subdivisions,
            surface_depth: surface_depth,
            unique_surface: unique_surface,
            unique_width: unique_width,
            text_alignment: text_alignment
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
    const input_text = document.querySelector("#input_text");
    const input_braille = document.querySelector("#input_braille");
    const stl_button = document.querySelector("#stl_button");
    const input_size = document.querySelector("#input_size");
    const input_spacing = document.querySelector("#input_spacing");
    const input_kerning = document.querySelector("#input_kerning");
    const input_subdivisions = document.querySelector("#input_subdivisions");
    const input_surface_depth = document.querySelector("#input_surface_depth");
    const input_unique_surface = document.querySelector("#input_unique_surface");
    const input_unique_width = document.querySelector("#input_unique_width");
    const input_text_alignment = document.querySelector("#input_text_alignment");

    input_text.addEventListener("input", encodeTextToBraille);
    input_braille.addEventListener("input", decodeBrailleToText);
    stl_button.addEventListener("click", downloadSTL);

    input_size.value = size;
    input_size.addEventListener("input", function(event) {
        size = parseFloat(event.target.value);
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
    });

    input_surface_depth.value = surface_depth;
    input_surface_depth.addEventListener("input", function(event) {
        surface_depth = parseFloat(event.target.value);
    });

    input_unique_surface.checked = unique_surface;
    input_unique_surface.addEventListener("input", function(event) {
        unique_surface = event.target.checked;
    });

    input_unique_width.checked = unique_width;
    input_unique_width.addEventListener("input", function(event) {
        unique_width = event.target.checked;
    });

    input_text_alignment.value = text_alignment;
    input_text_alignment.addEventListener("input", function(event) {
        text_alignment = event.target.value;
    });
});