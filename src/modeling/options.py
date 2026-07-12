"""Parameters that control how a Braille STL model is generated."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelOptions:
    resolution: int = 20
    plate_thickness: int = 2
    unique_plate: bool = False
    symbols_per_line: int = 20
    text_alignment: str = "left"
    rounded: bool = False
    points_only: bool = False
