from typing import List

from .color import Color


class ColorPalette:
    def __init__(self, palette: List[Color]):
        self._palette = palette

    def from_proportions(self, proportions: List[float]) -> Color:
        if len(proportions) != len(self._palette):
            raise ValueError("Proportions do not match palette")
        r = g = b = total = 0
        for (i, c) in enumerate(self._palette):
            r += proportions[i] * c.r
            g += proportions[i] * c.g
            b += proportions[i] * c.b
            total += proportions[i]
        return Color(int(r / total), int(g / total), int(b / total))

    def __len__(self):
        return len(self._palette)
