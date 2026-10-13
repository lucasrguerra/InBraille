"""Pydantic request models for the HTTP API.

Every field is bounded: these limits are the first line of defence against oversized
payloads and against requests that would make the 3D generator burn CPU or memory.
"""
from pydantic import BaseModel, Field, field_validator, model_validator

MAX_TEXT_LENGTH = 5000
MAX_BRAILLE_LENGTH = 3000
MAX_LINES = 100
MAX_LINE_LENGTH = 200
MAX_STL_COST = 3000  # filled cells x resolution; keeps one request to roughly 10 s and under 1 GB
ALPHABET_PATTERN = r"^(Brazilian|North American|Chinese)$"

_BRAILLE_BLOCK = range(0x2800, 0x2900)


class Text(BaseModel):
    text: str = Field(max_length=MAX_TEXT_LENGTH)
    alphabet: str | None = Field(default=None, pattern=ALPHABET_PATTERN)


class Braille(BaseModel):
    braille: str = Field(max_length=MAX_TEXT_LENGTH)
    alphabet: str | None = Field(default=None, pattern=ALPHABET_PATTERN)


class ToSTLRequest(BaseModel):
    braille: str = Field(min_length=1, max_length=MAX_BRAILLE_LENGTH)
    resolution: int | None = Field(default=None, ge=1, le=1000)
    plate_thickness: int | None = Field(default=None, ge=0, le=1000)
    unique_plate: bool | None = None
    symbols_per_line: int | None = Field(default=None, ge=0, le=1000)
    text_alignment: str | None = Field(default=None, pattern=r"^(left|center|right)$")
    rounded: bool | None = None
    points_only: bool | None = None

    @field_validator("braille")
    @classmethod
    def only_braille_cells(cls, value: str) -> str:
        lines = value.split("\n")
        if len(lines) > MAX_LINES:
            raise ValueError(f"at most {MAX_LINES} lines are allowed")
        for line in lines:
            if len(line) > MAX_LINE_LENGTH:
                raise ValueError(f"lines may have at most {MAX_LINE_LENGTH} cells")
            if any(ord(char) not in _BRAILLE_BLOCK for char in line):
                raise ValueError("only Braille pattern characters and line breaks are allowed")
        return value

    @model_validator(mode="after")
    def bounded_generation_cost(self):
        resolution = min(max(self.resolution or 20, 15), 50)
        filled_cells = sum(1 for char in self.braille if char not in ("\n", "\u2800"))
        if filled_cells * resolution > MAX_STL_COST:
            raise ValueError(
                f"model too large: reduce the text or the resolution (filled cells x resolution must be at most {MAX_STL_COST})"
            )
        return self
