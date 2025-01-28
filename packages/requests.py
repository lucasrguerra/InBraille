from pydantic import BaseModel



class Text(BaseModel):
    text: str
    alphabet: str | None = None



class Braille(BaseModel):
    braille: str
    alphabet: str | None = None



class ToSTLRequest(BaseModel):
    braille: str
    resolution: int | None = None
    plate_thickness: float | None = None
    unique_plate: bool | None = None
    unique_width: bool | None = None
    text_alignment: str | None = None
    rounded: bool | None = None