# Inclusive STL

## Introduction

This repository contains the code for the Inclusive STL project. The goal of this project is to make an translater for braille to text and text to braille and export the result to a STL file.

This project supports this braile alphabets:

- North American Braille
- Brazilian Braille

## Running the code

To run the code, you need to have Python 3 installed. You can run the code by executing the following command:

```bash
python3 main.py
or
python main.py
```

The service will start running on `http://localhost:3000`.

The API has the following endpoints:

- `/api/encode`: Translates a text to braille.
- `/api/decode`: Translates a braille to text.
- `/api/to-stl`: Exports the braille to a STL file.