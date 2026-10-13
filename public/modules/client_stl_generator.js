/**
 * Client-Side Parametric STL Generator for InBraille.
 * Generates binary STL 3D models directly in the user's browser in milliseconds,
 * eliminating server CPU load, network latency, and queue timeouts.
 */

export const Dimensions = {
    dots_radius: 1,
    dots_spacing: 2.7,
    dots_apparent_thickness: 0.65,
    cells_width: 4.7,
    cells_height: 7.4,
    cells_h_spacing: 6.6,
    cells_v_spacing: 10.8
};

const BRAILLE_CODE_MAP = {
    '⠁': '100000', '⠃': '110000', '⠉': '100100', '⠙': '100110', '⠑': '100010',
    '⠋': '110100', '⠛': '110110', '⠓': '110010', '⠊': '010100', '⠚': '010110',
    '⠅': '101000', '⠇': '111000', '⠍': '101100', '⠝': '101110', '⠕': '101010',
    '⠏': '111100', '⠟': '111110', '⠗': '111010', '⠎': '011100', '⠞': '011110',
    '⠥': '101001', '⠧': '111001', '⠺': '010111', '⠭': '101101', '⠽': '101111',
    '⠵': '101011', '⠴': '001011', '⠂': '010000', '⠆': '011000', '⠒': '010010',
    '⠲': '010011', '⠢': '010001', '⠖': '011010', '⠶': '011011', '⠦': '011001',
    '⠔': '001010', '⠮': '011101', '⠹': '100111', '⠯': '111101', '⠫': '110101',
    '⠼': '001111', '⠈': '000100', '⠩': '100101', '⠷': '111011', '⠾': '011111',
    '⠪': '010101', '⠻': '110111', '⠸': '000111', '⠬': '001101', '⠤': '001001',
    '⠡': '100001', '⠌': '001100', '⠿': '111111', '⠣': '110001', '⠜': '001110',
    '⠨': '000101', '⠠': '000001', '⠰': '000011', '⠱': '100011', '⠄': '001000',
    '⠐': '000010', '⣄': '011001'
};

export function codeFor(character) {
    if (BRAILLE_CODE_MAP[character]) {
        return BRAILLE_CODE_MAP[character];
    }
    const val = character.charCodeAt(0) - 0x2800;
    if (val >= 0 && val <= 0xff) {
        let bits = '';
        for (let b = 0; b < 6; b++) {
            bits += (val >> b) & 1 ? '1' : '0';
        }
        return bits;
    }
    return '000000';
}

function createBox(w, h, d) {
    const hw = w / 2, hh = h / 2, hd = d / 2;
    const verts = [
        [-hw, -hh, -hd], [hw, -hh, -hd], [hw, hh, -hd], [-hw, hh, -hd],
        [-hw, -hh, hd], [hw, -hh, hd], [hw, hh, hd], [-hw, hh, hd]
    ];
    const faces = [
        [0, 2, 1], [0, 3, 2], // bottom (-z)
        [4, 5, 6], [4, 6, 7], // top (+z)
        [0, 1, 5], [0, 5, 4], // front (-y)
        [2, 3, 7], [2, 7, 6], // back (+y)
        [0, 4, 7], [0, 7, 3], // left (-x)
        [1, 2, 6], [1, 6, 5]  // right (+x)
    ];
    return { verts, faces };
}

function createCap(radius, apparentThickness, resolution = 16) {
    const cutZ = radius - apparentThickness;
    const nRings = Math.max(3, Math.floor(resolution / 2));
    const nSegs = Math.max(8, resolution);
    const verts = [];
    const faces = [];

    // Base center vertex at (0, 0, 0)
    verts.push([0, 0, 0]);

    // Ring 0: base circle at z = 0
    const baseR = Math.sqrt(Math.max(0, radius * radius - cutZ * cutZ));
    for (let j = 0; j < nSegs; j++) {
        const theta = (j * 2 * Math.PI) / nSegs;
        verts.push([baseR * Math.cos(theta), baseR * Math.sin(theta), 0]);
    }
    // Base disk triangles (normal pointing -z)
    for (let j = 0; j < nSegs; j++) {
        const next = (j + 1) % nSegs;
        faces.push([0, 1 + next, 1 + j]);
    }

    // Dome rings from z=0 up to the apex
    const ringStarts = [1];
    for (let i = 1; i <= nRings; i++) {
        const ringZ = (i * apparentThickness) / nRings;
        const zOrig = ringZ + cutZ;
        const r = Math.sqrt(Math.max(0, radius * radius - zOrig * zOrig));
        const rStart = verts.length;
        ringStarts.push(rStart);

        if (i === nRings) {
            // Apex point at (0, 0, apparentThickness)
            verts.push([0, 0, apparentThickness]);
            const prevStart = ringStarts[i - 1];
            for (let j = 0; j < nSegs; j++) {
                const next = (j + 1) % nSegs;
                faces.push([prevStart + j, prevStart + next, rStart]);
            }
        } else {
            for (let j = 0; j < nSegs; j++) {
                const theta = (j * 2 * Math.PI) / nSegs;
                verts.push([r * Math.cos(theta), r * Math.sin(theta), ringZ]);
            }
            const prevStart = ringStarts[i - 1];
            for (let j = 0; j < nSegs; j++) {
                const next = (j + 1) % nSegs;
                faces.push([prevStart + j, prevStart + next, rStart + j]);
                faces.push([prevStart + next, rStart + next, rStart + j]);
            }
        }
    }
    return { verts, faces };
}

function createCylinder(radius, height, resolution = 16) {
    const verts = [];
    const faces = [];
    const hh = height / 2;
    const nSegs = Math.max(8, resolution);

    // Bottom center at (-radius, 0, -hh)
    verts.push([-radius, 0, -hh]); // index 0
    // Top center at (-radius, 0, hh)
    verts.push([-radius, 0, hh]);  // index 1

    for (let i = 0; i < nSegs; i++) {
        const theta = (i * 2 * Math.PI) / nSegs;
        const x = -radius + radius * Math.cos(theta);
        const y = radius * Math.sin(theta);
        verts.push([x, y, -hh]); // 2 + i * 2
        verts.push([x, y, hh]);  // 2 + i * 2 + 1
    }

    for (let i = 0; i < nSegs; i++) {
        const next = (i + 1) % nSegs;
        const b1 = 2 + i * 2;
        const t1 = 2 + i * 2 + 1;
        const b2 = 2 + next * 2;
        const t2 = 2 + next * 2 + 1;

        // Bottom cap (normal pointing -z)
        faces.push([0, b2, b1]);
        // Top cap (normal pointing +z)
        faces.push([1, t1, t2]);
        // Side quads
        faces.push([b1, b2, t1]);
        faces.push([b2, t2, t1]);
    }
    return { verts, faces };
}

function translateMesh(mesh, dx, dy, dz, rotXDeg = 0) {
    const rad = rotXDeg * (Math.PI / 180);
    const cos = Math.cos(rad), sin = Math.sin(rad);
    const newVerts = mesh.verts.map(([x, y, z]) => {
        const ny = y * cos - z * sin;
        const nz = y * sin + z * cos;
        return [x + dx, ny + dy, nz + dz];
    });
    return { verts: newVerts, faces: mesh.faces };
}

function mergeMeshes(meshes) {
    let totalVerts = 0;
    let totalFaces = 0;
    for (let i = 0; i < meshes.length; i++) {
        totalVerts += meshes[i].verts.length;
        totalFaces += meshes[i].faces.length;
    }

    const allVerts = new Array(totalVerts);
    const allFaces = new Array(totalFaces);

    let vOffset = 0;
    let fOffset = 0;
    for (let i = 0; i < meshes.length; i++) {
        const m = meshes[i];
        const mv = m.verts;
        const mf = m.faces;
        const currentVOffset = vOffset;

        for (let j = 0; j < mv.length; j++) {
            allVerts[vOffset + j] = mv[j];
        }
        for (let j = 0; j < mf.length; j++) {
            const face = mf[j];
            allFaces[fOffset + j] = [face[0] + currentVOffset, face[1] + currentVOffset, face[2] + currentVOffset];
        }

        vOffset += mv.length;
        fOffset += mf.length;
    }
    return { verts: allVerts, faces: allFaces };
}

function buildCell(code, radius, spacing, apparentThickness, resolution, pointsOnly) {
    const dot = createCap(radius, apparentThickness, resolution);
    const dotPositions = [
        [0, 2 * spacing],
        [0, spacing],
        [0, 0],
        [spacing, 2 * spacing],
        [spacing, spacing],
        [spacing, 0]
    ];
    const parts = [];
    for (let i = 0; i < dotPositions.length; i++) {
        if (code[i] === '1') {
            const [x, y] = dotPositions[i];
            parts.push(translateMesh(dot, x, y, 0));
        }
    }
    return parts.length > 0 ? mergeMeshes(parts) : { verts: [], faces: [] };
}

function meshToBinarySTL(mesh) {
    const triangleCount = mesh.faces.length;
    const buffer = new ArrayBuffer(84 + triangleCount * 50);
    const view = new DataView(buffer);
    view.setUint32(80, triangleCount, true); // little-endian triangle count

    let offset = 84;
    const verts = mesh.verts;
    const faces = mesh.faces;

    for (let i = 0; i < triangleCount; i++) {
        const face = faces[i];
        const v0 = verts[face[0]];
        const v1 = verts[face[1]];
        const v2 = verts[face[2]];

        // Normal via cross product (v1 - v0) x (v2 - v0)
        const d1x = v1[0] - v0[0], d1y = v1[1] - v0[1], d1z = v1[2] - v0[2];
        const d2x = v2[0] - v0[0], d2y = v2[1] - v0[1], d2z = v2[2] - v0[2];
        let nx = d1y * d2z - d1z * d2y;
        let ny = d1z * d2x - d1x * d2z;
        let nz = d1x * d2y - d1y * d2x;
        const len = Math.hypot(nx, ny, nz);
        if (len > 1e-12) {
            nx /= len; ny /= len; nz /= len;
        } else {
            nx = 0; ny = 0; nz = 0;
        }

        view.setFloat32(offset, nx, true);
        view.setFloat32(offset + 4, ny, true);
        view.setFloat32(offset + 8, nz, true);
        view.setFloat32(offset + 12, v0[0], true);
        view.setFloat32(offset + 16, v0[1], true);
        view.setFloat32(offset + 20, v0[2], true);
        view.setFloat32(offset + 24, v1[0], true);
        view.setFloat32(offset + 28, v1[1], true);
        view.setFloat32(offset + 32, v1[2], true);
        view.setFloat32(offset + 36, v2[0], true);
        view.setFloat32(offset + 40, v2[1], true);
        view.setFloat32(offset + 44, v2[2], true);
        // Attribute bytes (uint16) are initialized to 0
        offset += 50;
    }
    return buffer;
}

/**
 * Builds the complete Braille 3D model and exports as a binary STL ArrayBuffer.
 */
export function buildClientSTL(braille, options = {}) {
    const resolution = Math.max(12, Math.min(50, options.resolution || 20));
    const plateThickness = Math.max(2, Math.min(100, options.plate_thickness || 2));
    let uniquePlate = options.unique_plate !== undefined ? options.unique_plate : false;
    const symbolsPerLine = Math.max(8, Math.min(50, options.symbols_per_line || 22));
    const textAlignment = options.text_alignment || 'left';
    let rounded = options.rounded !== undefined ? options.rounded : false;
    let pointsOnly = options.points_only !== undefined ? options.points_only : false;

    if (pointsOnly) {
        uniquePlate = true;
        rounded = false;
    }

    const rules = Dimensions;
    const rawPhrases = braille.split('\n');
    const phrases = rawPhrases.length > 0 ? rawPhrases : [''];
    const numberOfPhrases = phrases.length;
    const plateWidth = ((symbolsPerLine - 1) * rules.cells_h_spacing) + rules.cells_width;
    const letterReferenceZ = pointsOnly ? 0 : plateThickness;
    const referenceZ = plateThickness / 2;
    const plateHeight = rules.cells_v_spacing;
    const borderSize = rules.cells_width;
    const borderCylinderXRef = -0.7;
    const borderPlateXRef = -(0.7 + (borderSize / 2));

    const borderCylinder = createCylinder(borderSize, plateThickness, resolution);

    const charCache = {};
    const sceneParts = [];

    for (let phraseIndex = 0; phraseIndex < phrases.length; phraseIndex++) {
        const phrase = phrases[phraseIndex];
        const phraseParts = [];
        const thisPhraseWidth = ((Math.max(1, phrase.length) - 1) * rules.cells_h_spacing) + rules.cells_width;

        if (!uniquePlate) {
            const thisPlateHeight = rules.cells_v_spacing * 2;
            const platePosX = plateWidth / 2;
            const platePosY = (plateHeight - rules.cells_height) / 2;
            const finalPlateWidth = plateWidth + rules.cells_v_spacing;

            const thisPlate = createBox(finalPlateWidth, thisPlateHeight, plateThickness);
            phraseParts.push(translateMesh(thisPlate, platePosX, platePosY, referenceZ));

            // Corner marker
            const marker = createCap(1.6, rules.dots_apparent_thickness, resolution);
            const cornerX = platePosX - (finalPlateWidth / 2) + 3.0;
            const cornerY = platePosY - (thisPlateHeight / 2) + 3.0;
            phraseParts.push(translateMesh(marker, cornerX, cornerY, plateThickness));

            if (rounded) {
                const halfPlateHeight = thisPlateHeight / 2;
                const borderPlate = createBox(borderSize, thisPlateHeight - borderSize * 2, plateThickness);

                phraseParts.push(translateMesh(borderCylinder, borderCylinderXRef, platePosY + halfPlateHeight - borderSize, referenceZ));
                phraseParts.push(translateMesh(borderCylinder, borderCylinderXRef + finalPlateWidth, platePosY + halfPlateHeight - borderSize, referenceZ));
                phraseParts.push(translateMesh(borderCylinder, borderCylinderXRef, platePosY - halfPlateHeight + borderSize, referenceZ));
                phraseParts.push(translateMesh(borderCylinder, borderCylinderXRef + finalPlateWidth, platePosY - halfPlateHeight + borderSize, referenceZ));
                phraseParts.push(translateMesh(borderPlate, borderPlateXRef - borderSize, platePosY, referenceZ));
                phraseParts.push(translateMesh(borderPlate, borderPlateXRef + finalPlateWidth, platePosY, referenceZ));
            }
        }

        for (let letterIndex = 0; letterIndex < phrase.length; letterIndex++) {
            const letter = phrase[letterIndex];
            if (letter === '⠀' || letter === ' ') continue;

            let letterPosY = -rules.dots_radius;
            let letterPosX = (letterIndex * rules.cells_h_spacing) + rules.dots_radius;
            let letterPosZ = letterReferenceZ;

            if (uniquePlate) {
                letterPosY -= phraseIndex * rules.cells_v_spacing;
            }

            if (textAlignment === 'center') {
                letterPosX += (plateWidth - thisPhraseWidth) / 2;
            } else if (textAlignment === 'right') {
                letterPosX += plateWidth - thisPhraseWidth;
            }

            if (!charCache[letter]) {
                charCache[letter] = buildCell(codeFor(letter), rules.dots_radius, rules.dots_spacing, rules.dots_apparent_thickness, resolution, pointsOnly);
            }
            if (charCache[letter].verts.length > 0) {
                phraseParts.push(translateMesh(charCache[letter], letterPosX, letterPosY, letterPosZ));
            }
        }

        if (phraseParts.length > 0) {
            const phraseMesh = mergeMeshes(phraseParts);
            const phrasePosZ = uniquePlate ? 0 : phraseIndex * (plateThickness + rules.cells_v_spacing);
            sceneParts.push(translateMesh(phraseMesh, 0, 0, phrasePosZ));
        }
    }

    if (uniquePlate && !pointsOnly) {
        const borderYRef = rules.cells_v_spacing + ((rules.cells_v_spacing - rules.cells_height) / 2);
        const finalPlateHeight = (numberOfPhrases * rules.cells_v_spacing) + rules.cells_v_spacing;
        const platePosX = plateWidth / 2;
        const platePosY = borderYRef - (finalPlateHeight / 2);
        const finalPlateWidth = plateWidth + rules.cells_v_spacing;

        const plate = createBox(finalPlateWidth, finalPlateHeight, plateThickness);
        sceneParts.push(translateMesh(plate, platePosX, platePosY, referenceZ));

        // Corner marker
        const marker = createCap(1.6, rules.dots_apparent_thickness, resolution);
        const cornerX = platePosX - (finalPlateWidth / 2) + 3.0;
        const cornerY = platePosY - (finalPlateHeight / 2) + 3.0;
        sceneParts.push(translateMesh(marker, cornerX, cornerY, plateThickness));

        if (rounded) {
            const borderPlate = createBox(borderSize, finalPlateHeight - borderSize * 2, plateThickness);
            sceneParts.push(translateMesh(borderCylinder, borderCylinderXRef, borderYRef - borderSize, referenceZ));
            sceneParts.push(translateMesh(borderCylinder, borderCylinderXRef + finalPlateWidth, borderYRef - borderSize, referenceZ));
            sceneParts.push(translateMesh(borderCylinder, borderCylinderXRef, borderYRef - finalPlateHeight + borderSize, referenceZ));
            sceneParts.push(translateMesh(borderCylinder, borderCylinderXRef + finalPlateWidth, borderYRef - finalPlateHeight + borderSize, referenceZ));
            sceneParts.push(translateMesh(borderPlate, borderPlateXRef - borderSize, platePosY, referenceZ));
            sceneParts.push(translateMesh(borderPlate, borderPlateXRef + finalPlateWidth, platePosY, referenceZ));
        }
    }

    if (pointsOnly && sceneParts.length > 0) {
        // Add orientation bar below lowest dots
        const preMesh = mergeMeshes(sceneParts);
        let xMin = Infinity, xMax = -Infinity, yMin = Infinity;
        for (let i = 0; i < preMesh.verts.length; i++) {
            const v = preMesh.verts[i];
            if (v[0] < xMin) xMin = v[0];
            if (v[0] > xMax) xMax = v[0];
            if (v[1] < yMin) yMin = v[1];
        }
        const barWidth = xMax - xMin;
        if (barWidth > 0 && isFinite(barWidth)) {
            const barDepth = 1.2;
            const barHeight = rules.dots_apparent_thickness;
            const barGap = 0.8;
            const bar = createBox(barWidth, barDepth, barHeight);
            sceneParts.push(translateMesh(
                bar,
                (xMin + xMax) / 2,
                yMin - barGap - (barDepth / 2),
                barHeight / 2
            ));
        }
    }

    const combinedMesh = sceneParts.length > 0 ? mergeMeshes(sceneParts) : { verts: [], faces: [] };
    // Final rotate 90 degrees around X axis: (x, y, z) -> (x, -z, y)
    const finalRotatedMesh = translateMesh(combinedMesh, 0, 0, 0, 90);
    return meshToBinarySTL(finalRotatedMesh);
}
