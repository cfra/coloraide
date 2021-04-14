"""Colors."""
from .srgb import SRGB
from .hsl import HSL
from .hwb import HWB
from .lab import LAB
from .lch import LCH
from ...colors import Color as GenericColor

CSS_OVERRIDES = (HSL, HWB, LAB, LCH, SRGB)


class Color(GenericColor):
    """Color wrapper class."""

    CS_MAP = {key: value for key, value in GenericColor.CS_MAP.items()}
    for color in CSS_OVERRIDES:
        CS_MAP[color.space()] = color
