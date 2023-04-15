from __future__ import annotations

from math import sqrt

MAX = 255


class Color:
    def __init__(self, r: int, g: int, b: int):
        if r < 0 or r > MAX or g < 0 or g > MAX or b < 0 or b > MAX:
            raise ValueError("Parameters out of range")
        self._r = r
        self._g = g
        self._b = b

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    def __repr__(self):
        return f"#{hex(self._r).lstrip('0x')}{hex(self._g).lstrip('0x')}{hex(self._b).lstrip('0x')}"

    def distance(self, other: Color) -> float:
        return sqrt((self._b - other._b)**2 + (self._g - other._g)**2 + (self._g - other._g)**2)
