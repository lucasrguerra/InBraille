from pydantic import BaseModel



class Text(BaseModel):
    text: str
    alphabet: str | None = None



class Braille(BaseModel):
    braille: str
    alphabet: str | None = None



class ToSTLRequest(BaseModel):
    braille: str
    radius: float | None = None
    spacing: float | None = None
    kerning: float | None = None
    subdivisions: int | None = None
    thickness: float | None = None
    unique_plate: bool | None = None
    unique_width: bool | None = None
    text_alignment: str | None = None
    rounded: bool | None = None