# InBraille

## Introduction

This repository contains the code for the InBraille project.

InBraille is an innovative Brazilian tool from Pernambuco that converts texts to Braille and exports them in both ASCII format and in STL plates for 3D printing. With this solution, it is possible to increase accessibility and inclusion, allowing anyone to create tactile materials for people with visual impairments.

In addition to being an accessible and easy-to-use technology, this project has a significant social impact, enabling the production of texts, labels, informational signs and educational materials in Braille in an accessible and personalized way. Whether for educational, professional or everyday purposes, this tool aims to make information truly universal. The goal is to democratize access to Braille through maker culture and 3D printing, providing autonomy and independence to those who need it.

### Supported Braille Alphabets:

- **Brazilian Braille** (with native warning regarding ambiguous characters)
- **North American Braille**
- **Chinese (Mandarin) Braille** (supporting Pinyin and Chinese characters input, with localized input assistance)

---

## Key Features

1. **Unified HTML Template**: Single, consolidated `index.html` structure served for all routes.
2. **Dynamic Client-Side Localization (i18n)**: Fully translates the interface dynamically without page reloads across Portuguese, English, and Chinese.
3. **Modular Frontend (SOLID Principles)**: Deconstructed frontend architecture divided into clean, single-responsibility ES Modules:
   - `state.js`: Centralized application state tracking.
   - `i18n.js`: Localized DOM translations and menu management.
   - `ui.js`: Reusable visual components (toasts, focus highlights).
   - `converter.js`: Conversion flows and line-length validators.
   - `stl.js`: 3D parameters control and STL file compiler.
   - `index.js`: Orchestrator entry point.
4. **Standardized Premium UI Warnings**: Consistent, modern side-border alert cards for warnings and tips.

---

## Backend Architecture (`src/`)

The Python backend is organized into domain-driven subdirectories under `src/`, utilizing **FastAPI** for web routing and **VTK (Visualization Toolkit)** for 3D modeling:

### 1. Domain Model (`src/domain/`)
Core representations and mathematical constants of the Braille system:
- `alphabets.py`: Mappings for Brazilian and North American character-to-cell associations.
- `chinese_braille.py`: Constants and lists representing tones, initial and final syllables, and punctuation for Chinese Braille.
- `braille_codes.py`: Converts characters to 6-dot/8-dot binary matrices and Unicode Braille patterns.
- `dimensions.py`: Defines dimensions of Braille cells (dot radius, height, horizontal and vertical spacing).

### 2. Translation Engine (`src/translation/`)
Core encoders/decoders translating between text and Unicode Braille:
- `translator.py`: Router that delegates request conversion depending on selected alphabet.
- `encoder.py` / `decoder.py`: Translate between standard characters/Hanzi/Pinyin and Braille Unicode cells (PT/EN/ZH). The Chinese translation parses Chinese Hanzi or pinyin using `pypinyin` to analyze polyphonic contexts, compiling them into syllables (initial + final + tone combinations) according to official Chinese Braille rules.

### 3. 3D Modeling and Mesh Engine (`src/modeling/`)
Decoupled geometry generation and composition system:
- `mesh_engine.py`: Defines the abstract `MeshEngine` wrapper interface, decoupling layout modeling logic from the underlying 3D graphics library.
- `model_builder.py`: Composites the physical shapes. Places plate bases, rounded borders, spherical dot caps, orientation markers, and orientation bars (in "dots only" mode).
- `options.py`: Defines settings configuration (symbols per line, plate thickness, resolution).
- `stl_service.py`: Standardizes generation inputs and exports binary STL models.

### 4. 3D Rendering & Serializer (`src/rendering/`)
Concrete implementation of the graphics pipeline:
- `vtk_mesh_engine.py`: VTK-based implementation of `MeshEngine` drawing cubes, spheres, cylinders, and sphere-cap clips.
- `vtk_stl_serializer.py`: Serializes VTK PolyData objects into raw binary STL file format.

### 5. Web API Layers (`src/web/`)
Web service routing and schemas:
- `app.py`: Initiates the FastAPI application instance.
- `api_routes.py`: Implements REST API controllers (`/api/encode`, `/api/decode`, `/api/to-stl`).
- `schemas.py`: Pydantic request body schemas.
- `page_routes.py`: Serves static assets and maps `/`, `/en`, and `/zh` requests dynamically to serve the root `index.html` template.

---

## Running the code

To run the code, you need to have Python 3 installed. You can run the code by executing the following command:

```bash
python -m venv venv
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

The service will start running on `http://localhost:3000`.

The API has the following endpoints:

- `/api/encode`: Translates a text to braille.
- `/api/decode`: Translates a braille to text.
- `/api/to-stl`: Exports the braille text to plate in STL format.

---

## License and Credits

This project is licensed under the MIT License. It was developed by [Lucas Rayan Guerra](https://github.com/lucasrguerra).