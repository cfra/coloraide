"""
CAM16 class.

https://www.imaging.org/site/PDFS/Papers/2000/PICS-0-81/1611.pdf
https://observablehq.com/@jrus/cam16
https://arxiv.org/abs/1802.06067
https://doi.org/10.1002/col.22131
"""
from __future__ import annotations
import math
from .cam16_jmh import CAM16JMh, xyz_d65_to_cam16, cam16_to_xyz_d65, Environment
from ..spaces import Space, Labish
from ..cat import WHITES
from ..channels import Channel, FLG_MIRROR_PERCENT
from .. import util
from ..types import Vector
from .. import algebra as alg


def cam16_jmh_to_cam16_jab(jmh: Vector, env: Environment) -> Vector:
    """Translate a CAM16 JMh to Jab of the same viewing conditions."""

    J, M, h = jmh

    if J == 0.0:
        return [0.0, 0.0, 0.0]

    # Account for negative colorfulness by reconverting
    if M < 0:
        cam16 = xyz_d65_to_cam16(cam16_to_xyz_d65(J=J, M=M, h=h, env=env), env=env)
        J, M, h = cam16[0], cam16[5], cam16[2]

    return [
        J,
        M * math.cos(math.radians(h)),
        M * math.sin(math.radians(h))
    ]


def cam16_jab_to_cam16_jmh(jab: Vector) -> Vector:
    """Translate a CAM16 Jab to JMh of the same viewing conditions."""

    J, a, b = jab

    if J == 0.0:
        return [0.0, 0.0, 0.0]

    M = math.sqrt(a ** 2 + b ** 2)
    h = math.degrees(math.atan2(b, a))

    return [J, M, util.constrain_hue(h)]


class CAM16(Labish, Space):
    """CAM16 class (Jab)."""

    BASE = "cam16-jmh"
    NAME = "cam16"
    SERIALIZE = ("--cam16",)
    CHANNELS = (
        Channel("j", 0.0, 100.0),
        Channel("a", -90.0, 90.0, flags=FLG_MIRROR_PERCENT),
        Channel("b", -90.0, 90.0, flags=FLG_MIRROR_PERCENT)
    )
    CHANNEL_ALIASES = {
        "lightness": "j"
    }
    WHITE = WHITES['2deg']['D65']
    # Use the same environment as CAM16JMh
    ENV = CAM16JMh.ENV
    ACHROMATIC = CAM16JMh.ACHROMATIC
    INV_ACHROMATIC = CAM16JMh.INV_ACHROMATIC

    def resolve_channel(self, index: int, coords: Vector) -> float:
        """Resolve channels."""

        if index in (1, 2):
            # Assume black if J is below zero
            J = coords[0]

            achromatic = self.INV_ACHROMATIC if J < 0 else self.ACHROMATIC

            if not math.isnan(coords[index]):
                return coords[index]

            return achromatic.get_ideal_ab(J)[index - 1]

        value = coords[index]
        return self.channels[index].nans if math.isnan(value) else value

    def is_achromatic(self, coords: Vector) -> bool:
        """Check if color is achromatic."""

        j = coords[0]
        m, h = alg.rect_to_polar(coords[1], coords[2])

        if j == 0.0:
            return True

        if j < 0.0:
            return self.INV_ACHROMATIC.test(j, m, h)

        return self.ACHROMATIC.test(j, m, h)

    def to_base(self, coords: Vector) -> Vector:
        """To CAM16 JMh from CAM16."""

        return cam16_jab_to_cam16_jmh(coords)

    def from_base(self, coords: Vector) -> Vector:
        """From CAM16 JMh to CAM16."""

        return cam16_jmh_to_cam16_jab(coords, self.ENV)
