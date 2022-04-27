# Filters

ColorAide implements a number of filters implemented as plugins. The first set of filters mirror those found in the W3C
[Filter Effects Module Level 1][filter-effects] specification, specifically the filters that directly apply to colors.
The second set of filters simulate color vision deficiencies.

## W3C Filter Effects

The following filters are all supported in ColorAide and generally adhere to the specification in regards to behavior.
By default, filters are applied in the Linear sRGB color space, but can be applied in sRGB if requested. All other
color spaces will throw an error.

=== "Normal"

    ![Normal](./images/color-wheel.png)

=== "Brightness"

    ![Brightness](./images/color-wheel-brightness.png)

=== "Saturate"

    ![Saturate](./images/color-wheel-saturate.png)

=== "Contrast"

    ![Contrast](./images/color-wheel-contrast.png)

=== "Opacity"

    ![Opacity](./images/color-wheel-opacity.png){.trans-bg}

=== "Invert"

    ![Invert](./images/color-wheel-invert.png)

=== "Hue Rotate"

    ![Hue Rotate](./images/color-wheel-hue-rotate.png)

=== "Sepia"

    ![Sepia](./images/color-wheel-sepia.png)

=== "Grayscale"

    ![Grayscale](./images/color-wheel-grayscale.png)

In ColorAide, just call the `filter` method and provide the name of the filter. If not `amount` is provided, the default
according to the W3C spec will be used instead.

```playground
inputs = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
colors = Color(inputs[0]).steps(inputs[1:], steps=10, space='srgb')
colors
ColorRow()
[c.filter('brightness', 0.5).clip() for c in colors]
ColorRow()
[c.filter('saturate', 0.5).clip() for c in colors]
ColorRow()
[c.filter('contrast', 1.2).clip() for c in colors]
ColorRow()
[c.filter('opacity', 0.5).clip() for c in colors]
ColorRow()
[c.filter('invert', 1).clip() for c in colors]
ColorRow()
[c.filter('hue-rotate', 90).clip() for c in colors]
ColorRow()
[c.filter('sepia', 1).clip() for c in colors]
ColorRow()
[c.filter('grayscale', 1).clip() for c in colors]
```

## Color Vision Deficiency Simulation

Color blindness or color vision deficiency (CVD) affects approximately 1 in 12 men (8%) and 1 in 200 women. CVD affects
millions of people in the world, and many people have no idea that they are color blind and not seeing the full spectrum
that others see.

CVD simulation allows those who do not suffer with one of the many different variations of color blindness, to simulate
what someone with a CVD would see. Keep in mind that these are just approximations, and that a given type of CVD can be
quite different from person to person in severity.

The human eye has 3 types of cones that are used to perceive colors. Each of these cones can become deficient, either
through genetics, or other means. Each type of cone is responsible for perceiving either red, green, or blue colors. A
CVD occurs when one or more of these cones are missing or not functioning properly. There are sever cases where one of
the three cones will not perceive color at all, and there are others were the cones may just be less sensitive.

### Dichromacy

Dichromacy is a type of CVD that has the characteristics of essentially causing the person to only have two functioning
cones for perceiving colors. This essentially flattens the color spectrum into a 2D plane. Protanopia describes the CVD
where the cone responsible for red light does not function, deuteranopia describes the CVD affecting the green cone, and
tritanopia describes deficiencies with the blue cone.

=== "Normal"

    ![Normal](./images/color-wheel.png)

=== "Protanopia"

    ![Protanopia](./images/color-wheel-protan.png)

=== "Deuteranopia"

    ![Deuteranopia](./images/color-wheel-deutan.png)

=== "Tritanopia"

    ![Tritanopia](./images/color-wheel-tritan.png)

By default, ColorAide uses the [Brettel 1997 method][brettel] to simulate tritanopia and the
[Viénot, Brettel, and Mollon 1999 approach][vienot] to simulate protanopia and and deuteranopia. While Brettel is
probably the best approach for all cases, Viénot is much faster and does quite well for protanopia and deuteranopia.

```playground
inputs = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
colors = Color(inputs[0]).steps(inputs[1:], steps=10, space='srgb')
colors
ColorRow()
[c.filter('protan').clip() for c in colors]
ColorRow()
[c.filter('deutan').clip() for c in colors]
ColorRow()
[c.filter('tritan').clip() for c in colors]
```

If desired, any of the three available methods can be used. Brettel is usually considered best option for accuracy.
Viénot is faster and does quite well for protanopia and deuteranopia, but is not quite as accurate for tritanopia.
[Machado 2009][machado] has better logic for severity ranges less than 1, but is probably even further off for
tritanopia.

```playground
inputs = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
colors = Color(inputs[0]).steps(inputs[1:], steps=10, space='srgb')
colors
ColorRow()
[c.filter('tritan', method='brettel').clip() for c in colors]
ColorRow()
[c.filter('tritan', method='vienot').clip() for c in colors]
ColorRow()
[c.filter('tritan', method='machado').clip() for c in colors]
```

### Anomalous Trichromacy

While Dichromacy is probably the more sever case with only two functional cones, a more common CVD type is anomalous
trichromacy. In this case, a person will have three functioning cones, but not all of the cones function with full
sensitivity. Sometimes, the sensitivity can be so low, that their ability to perceive color may be close to someone with
dichromacy.

While dichromacy may be considered a severity 1, a given case of anomalous trichromacy could be anywhere between 0 and
1, where 0 would be no CVD.

Like dichromacy, the related deficiencies are named in a similar manner: protanomaly (reduced red sensitivity),
deuteranomaly (reduced green sensitivity), and tritanomaly (reduced blue sensitivity).

=== "Normal"

    ![Normal](./images/color-wheel.png)

=== "Protanomaly Severity 0.5"

    ![Protanomaly 0.5](./images/color-wheel-protan-machado-0.5.png)

=== "Protanomaly Severity 0.7"

    ![Protanomaly 0.7](./images/color-wheel-protan-machado-0.7.png)

=== "Protanomaly Severity 0.9"

    ![Protanomaly 0.9](./images/color-wheel-protan-machado-0.9.png)

To represent anomalous trichromacy, ColorAide leans on the [Machado 2009 approach][machado] which has a more nuanced
approach to handling severity levels below 1. This approach did not really focus on tritanopia though, and the suggested
algorithm for tritanopia should only be considered as an approximation. Instead of relying on the Machado approach for
tritanomaly, we instead just use linear interpolation between the severity 1 results and the severity 0 (no CVD)
results. With that said, the `method` can always be overridden to use something other than the defaults.

```playground
inputs = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
colors = Color(inputs[0]).steps(inputs[1:], steps=10, space='srgb')
colors
ColorRow()
[c.filter('protan', 0.75).clip() for c in colors]
ColorRow()
[c.filter('deutan', 0.75).clip() for c in colors]
ColorRow()
[c.filter('tritan', 0.75).clip() for c in colors]
```

## Usage Details

To use filters, a filter name must be given, followed by an optional amount. If an amount is omitted, suitable default
will be used. The exact range a given filter accepts varies depending on the filter. If a value exceeds the filter range
, the value will be clamped.

Filters       | Name         | Default
------------- | ------------ | -------
Brightness    | `brightness` | `#!py3 1`
Saturation    | `saturate`   | `#!py3 1`
Contrast      | `contrast`   | `#!py3 1`
Opacity       | `opacity`    | `#!py3 1`
Invert        | `invert`     | `#!py3 1`
Hue\ rotation | `hue-rotate` | `#!py3 0`
Sepia         | `sepia`      | `#!py3 1`
Grayscale     | `grayscale`  | `#!py3 1`
Protan        | `protan`     | `#!py3 1`
Deutan        | `deutan`     | `#!py3 1`
Tritan        | `tritan`     | `#!py3 1`

All of the filters that are supported allow filtering in the Linear sRGB color space and will do so by default.
Additionally, the W3C filter effects also support filtering in the sRGB color space. The CVD filters are specifically
designed to be applied in the Linear sRGB space, and cannot be used in any other color space.

```playground
inputs = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
colors = Color(inputs[0]).steps(inputs[1:], steps=10, space='srgb')
colors
ColorRow()
[c.filter('sepia', 1, space='srgb-linear').clip() for c in colors]
ColorRow()
[c.filter('sepia', 1, space='srgb').clip() for c in colors]
```

!!! tip "Processing Lots of Colors"
    One logical application for filters is to apply them directly to images. If you are performing these operations on
    millions of pixels, you may notice that ColorAide, with all of its convenience, may not always be the fastest. There
    is a cost due to the overhead of convenience and a cost due to the pure Python approach as well. With that said,
    there are tricks that can dramatically make things much faster!

    `functools.lru_cache` is your friend in such cases. We actually process all the images on this page with ColorAide
    to demonstrate the filters. The key to making it a quick and painless process was to cache repetitive operations.
    When processing images, it is highly likely that you will be performing the same operations on thousands of
    identical pixels. Caching the work you've already done can speed this process up exponentially in most cases.
    Though, images with an abnormal amount of unique, non consecutive pixels may not perform as well.

    We can crawl the pixels in a file, and using a simple function like below, we will only process a pixel once (at
    least until our cache fills and we start having to overwrite existing colors).

    ```py
    @lru_cache(maxsize=1024 * 1024)
    def apply_filter(name, amount, space, method, p):
        """Apply filter."""

        has_alpha = len(p) > 3
        color = Color('srgb', [x / 255 for x in p[:3]], p[3] / 255 if has_alpha else 1)
        if method is not None:
            # This is a CVD filter that allows specifying the method
            color.filter(name, amount, space=space, in_place=True, method=method)
        else:
            # General filter.
            color.filter(name, amount, space=space, in_place=True)
        # We could gamut map or just do a simple clip, we've opted for a simple fast clip for now.
        color.clip(in_place=True)
        return tuple([int(x * 255) for x in color[:-1]]) + ((int(color[-1] * 255),) if has_alpha else tuple())
    ```

    For us, it turned a ~8 minute process into a ~35 second process^\*^.

    The full script can be viewed [here](https://github.com/facelessuser/coloraide/blob/master/tools/filters.py).

    \* _Tests were performed using the [Pillow][pillow] library. Results may vary depending on the size of the image,
    pixel configuration, number of unique pixels, etc. Cache size can be tweaked to optimize the results._

<style>
img.trans-bg {
    background-color: var(--swatch-bg-color);
    background-image: linear-gradient(45deg,var(--swatch-bg-alt-color) 25%,transparent 25%),linear-gradient(-45deg,var(--swatch-bg-alt-color) 25%,transparent 25%),linear-gradient(45deg,transparent 75%,var(--swatch-bg-alt-color) 75%),linear-gradient(-45deg,transparent 75%,var(--swatch-bg-alt-color) 75%);
    background-position: 0 0,0 0.5em,0.5em -0.5em,-0.5em 0;
    background-size: 1em 1em;
}
</style>