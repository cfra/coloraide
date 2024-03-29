"""Test gamut mapping response."""
import sys
import os
import argparse
import itertools as it

sys.path.insert(0, os.getcwd())

from coloraide.everything import ColorAll as Color  # noqa: E402


def run(gamut, space, max_chroma):
    """Test the gamut mapping algorithm noting the ∆L, ∆h, and the worst ∆h offender."""

    max_delta_h = 0
    max_delta_l = 0
    worst = None
    lch = Color('white').convert(space)
    l, _, h = lch._space.indexes()
    scale = lch[l] / 100

    for light in range(0, 100):
        for hue in range(360):
            c1 = Color(space, [light * scale, max_chroma, hue / 2])
            c2 = c1.clone().fit(gamut, method='raytrace', lch=space)
            dl = (c1[l] - c2[l])
            if abs(dl) > abs(max_delta_l):
                max_delta_l = dl

            h1, h2 = c1[h], c2[h]
            dh = (h1 - h2)
            if dh > 180:
                dh -= 360
            elif dh < -180:
                dh += 360
            if abs(dh) > abs(max_delta_h):
                max_delta_h = dh
                worst = c1

    print(f'=== Far: Chroma {max_chroma} ===')
    print('∆L =', max_delta_l)
    print('∆h =', max_delta_h)
    print('Worst ∆h offender =>', worst)

    far_delta_h = max_delta_h
    far_delta_l = max_delta_l
    far_worst = worst

    max_delta_h = 0
    max_delta_l = 0
    worst = None

    for r, g, b in it.product(range(101), range(101), range(101)):
        c1 = Color('display-p3', [r / 100, g / 100, b / 100]).convert(space)
        c2 = c1.clone().fit(gamut, method='raytrace', lch=space)
        dl = (c1[l] - c2[l])
        if abs(dl) > abs(max_delta_l):
            max_delta_l = dl

        h1, h2 = c1[h], c2[h]
        dh = (h1 - h2)
        if dh > 180:
            dh -= 360
        elif dh < -180:
            dh += 360
        if abs(dh) > abs(max_delta_h):
            max_delta_h = dh
            worst = c1

    print('=== Near: Display-P3 to sRGB ===')
    print('∆L =', max_delta_l)
    print('∆h =', max_delta_h)
    print('Worst ∆h offender =>', worst)

    if abs(far_delta_h) > abs(max_delta_h):
        max_delta_h = far_delta_h
        worst = far_worst
    if abs(far_delta_l) > abs(max_delta_l):
        max_delta_l = far_delta_l

    print('=== Final ===')
    print('∆L =', max_delta_l)
    print('∆h =', max_delta_h)
    print('Worst ∆h offender =>', worst)


def main():
    """Main."""

    parser = argparse.ArgumentParser(
        prog='gamutcheck.py',
        description='Check gamut mapping using ray tracing.'
    )
    # Flag arguments
    parser.add_argument(
        '--lch', '-l', default='oklch', help="LCh space to use as the mapping space."
    )
    parser.add_argument(
        '--gamut', '-g', default='display-p3', help="Gamut to test.",
    )
    parser.add_argument(
        '--max-chroma', '-c', type=float, default=0.8, help="Max chroma to test GMA with."
    )
    args = parser.parse_args()

    run(args.gamut, args.lch, args.max_chroma)

    return 0


if __name__ == "__main__":
    sys.exit(main())
