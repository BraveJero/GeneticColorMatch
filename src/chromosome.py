from __future__ import annotations

from copy import copy
from typing import List

from .gene import Gene


class Chromosome:
    def __init__(self, information: List[Gene]):
        self._information = copy(information)

    @property
    def information(self) -> List[Gene]:
        return self._information

    def __repr__(self):
        return self._information.__repr__()
