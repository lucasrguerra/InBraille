from pydantic import BaseModel

class Text(BaseModel):
    text: str

class Braille(BaseModel):
    braille: str

class ToSTLRequest(BaseModel):
    braille: str
    size: float | None = None
    spacing: float | None = None
    kerning: float | None = None
    subdivisions: int | None = None
    surface_depth: float | None = None
    unique_surface: bool | None = None
    unique_width: bool | None = None
    text_alignment: str | None = None