# InBraille

## Introduction

This repository contains the code for the InBraille project.

InBraille is an innovative tool from Pernambuco that converts texts to Braille and exports them in both ASCII format and in STL plates for 3D printing. With this solution, it is possible to increase accessibility and inclusion, allowing anyone to create tactile materials for people with visual impairments.

In addition to being an accessible and easy-to-use technology, this project has a significant social impact, enabling the production of texts, labels, informational signs and educational materials in Braille in an accessible and personalized way. Whether for educational, professional or everyday purposes, this tool aims to make information truly universal. The goal is to democratize access to Braille through maker culture and 3D printing, providing autonomy and independence to those who need it.

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
- `/api/to-stl`: Exports the braille text to plate in STL format.