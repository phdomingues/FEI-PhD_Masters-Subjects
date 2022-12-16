from __future__ import annotations

from enum import Enum, auto

class Color(Enum):
    BLACK = auto()
    BLUE = auto()
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    PURPLE = auto()
    WHITE = auto()
    END_COLOR = auto()
    UNKNOWN = auto()

    @staticmethod
    def color2ascii(color:Color) -> str:
        proxy = {
            Color.BLACK : "\033[0;40m",
            Color.RED : "\033[0;41m",
            Color.GREEN : "\033[0;42m",
            Color.BLUE : "\033[0;44m",
            Color.PURPLE : "\033[0;45m",
            Color.WHITE : "\033[0;47m",
            Color.YELLOW : "\033[1;43m",
            Color.END_COLOR : "\033[0m",
            Color.UNKNOWN: ""
        }
        return proxy.get(color, '')
