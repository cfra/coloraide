"""Modify a picture by increasing chroma and applying gamut mapping."""
from functools import lru_cache
from PIL import Image
import time
import argparse
import sys
import os

# We want to load ColorAide from the working directory to pick up the version under development
sys.path.insert(0, os.getcwd())

try:
    from coloraide_extras.everything import ColorAll as Color
except ImportError:
    from coloraide.everything import ColorAll as Color


def printt(t):
    """Print time."""

    print('Completed in: ', end='')
    s = t // 1e+9
    m = t // 1e+6
    u = t // 1000
    if s:
        s = t / 1e+9
        h = m = 0
        m = s // 60
        if m:
            s -= m * 60
            h = m // 60
            if h:
                m -= h * 60
        if h:
            print('{} hours '.format(h), end='')
        if m:
            print('{} minutes '.format(m), end='')
        print('{} sec'.format(s))
    elif m:
        print('{} msec'.format(t / 1e+6))
    elif u:
        print('{} usec'.format(t / 1000))
    else:
        print('{} nsec'.format(t))


@lru_cache(maxsize=1024 * 1024)
def apply_gamut_map(amount, p, fit):
    """Apply filter."""

    has_alpha = len(p) > 3
    color = Color('srgb', [x / 255 for x in p[:3]], p[3] / 255 if has_alpha else 1)
    color.set('oklch.c', lambda c: c * amount)
    # Fit the color back into the color gamut and return the results
    return tuple(int(x * 255) for x in color.fit(method=fit)[:4 if has_alpha else -1])


def process_image(img, output, amount, fit):
    """Process the image applying the requested filter."""

    with Image.open(img) as im:

        # Make sure we are writing in transparent mode for the opacity filter
        if im.format == 'PNG':
            if im.mode not in ('RGBA',):
                im = im.convert('RGBA')

        pixels = im.load()
        start = time.perf_counter_ns()
        total = im.size[0] * im.size[1]
        factor = 100 / total
        i = j = 0
        print('Pixels: {}'.format(total))
        print('> 0%', end='\r')
        for i in range(im.size[0]):
            for j in range(im.size[1]):
                pixels[i, j] = apply_gamut_map(amount, pixels[i, j], fit)
            print('> {}%'.format(int((i * j) * factor)), end="\r")
        print('> 100%')
        t = time.perf_counter_ns() - start
        printt(t)
        im.save(output)


def main():
    """Main."""

    parser = argparse.ArgumentParser(
        prog='apply_gamut.py',
        description='Force higher chroma and apply gamut mapping to an image.'
    )
    parser.add_argument('--input', '-i', help='Input image.')
    parser.add_argument('--output', '-o', help='Output name and location.')
    parser.add_argument('--amount', '-a', type=float, help='Amount to increase chroma.')
    parser.add_argument('--gamut-map', '-g', default="clip", help="Specify GMA method to use (default simple clipping)")
    args = parser.parse_args()

    process_image(
        args.input,
        args.output,
        args.amount,
        args.gamut_map
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
