import * as THREE from "three";
import { STLLoader } from "three/addons/loaders/STLLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

// The dots stick out 0.65 mm beyond the plate's front face (apparent thickness).
// After the model's 90° rotation this protrusion is along -Y, so any surface whose
// Y is below (plate_front = minY + 0.65) belongs to a dot / orientation marker.
const APPARENT_THICKNESS = 0.65;
const PLATE_COLOR = new THREE.Color(0x8b5cf6); // purple
const DOT_COLOR = new THREE.Color(0xf59e0b);   // amber

let state = null;

function init(container) {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf3f4f6);

    const camera = new THREE.PerspectiveCamera(
        40,
        container.clientWidth / container.clientHeight,
        0.1,
        5000
    );
    camera.up.set(0, 0, 1);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;

    // Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.8));
    const keyLight = new THREE.DirectionalLight(0xffffff, 1.0);
    keyLight.position.set(0.5, -1, 1);
    scene.add(keyLight);
    const fillLight = new THREE.DirectionalLight(0xffffff, 0.45);
    fillLight.position.set(-1, 0.5, 0.5);
    scene.add(fillLight);

    state = { scene, camera, renderer, controls, container, mesh: null };

    function animate() {
        state.rafId = requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    const resize = () => {
        if (!container.clientWidth || !container.clientHeight) { return; }
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    };
    window.addEventListener("resize", resize);
    state.resize = resize;
}

function paintByHeight(geometry) {
    geometry.computeBoundingBox();
    const box = geometry.boundingBox;
    // The plate's front face sits exactly at (min.y + APPARENT_THICKNESS); pull the
    // threshold slightly below it so that flat face stays "plate" and only the dots
    // that protrude past it are colored as dots.
    const threshold = box.min.y + APPARENT_THICKNESS - 0.05;

    const position = geometry.attributes.position;
    const colors = new Float32Array(position.count * 3);
    for (let i = 0; i < position.count; i++) {
        const color = position.getY(i) < threshold ? DOT_COLOR : PLATE_COLOR;
        colors[i * 3] = color.r;
        colors[i * 3 + 1] = color.g;
        colors[i * 3 + 2] = color.b;
    }
    geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
}

function frameModel() {
    const { camera, controls, mesh, container } = state;

    const box = new THREE.Box3().setFromObject(mesh);
    const size = box.getSize(new THREE.Vector3());
    const aspect = container.clientWidth / container.clientHeight;
    const fov = (camera.fov * Math.PI) / 180;

    // We look along -Y: on screen the width is X and the height is Z.
    const fitHeight = (size.z / 2) / Math.tan(fov / 2);
    const fitWidth = (size.x / 2) / (Math.tan(fov / 2) * aspect);
    const distance = Math.max(fitHeight, fitWidth) * 1.15;

    controls.target.set(0, 0, 0);
    // Mostly a front view (looking along +Y), with a slight tilt so the dots read as 3D.
    camera.position.set(distance * 0.08, -distance, distance * 0.16);
    camera.near = Math.max(distance / 1000, 0.01);
    camera.far = distance * 100;
    camera.updateProjectionMatrix();
    controls.update();
}

window.renderSTLPreview = function (arrayBuffer) {
    const container = document.getElementById("stl_preview_canvas");
    if (!container) { return; }
    if (!state) { init(container); }

    if (state.mesh) {
        state.scene.remove(state.mesh);
        state.mesh.geometry.dispose();
        state.mesh.material.dispose();
        state.mesh = null;
    }

    const geometry = new STLLoader().parse(arrayBuffer);
    geometry.computeVertexNormals();
    geometry.center();
    paintByHeight(geometry);

    const material = new THREE.MeshStandardMaterial({
        vertexColors: true,
        metalness: 0.1,
        roughness: 0.55
    });
    const mesh = new THREE.Mesh(geometry, material);
    state.scene.add(mesh);
    state.mesh = mesh;

    frameModel();
    state.resize();
};
