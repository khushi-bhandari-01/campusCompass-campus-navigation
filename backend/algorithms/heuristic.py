import math
from typing import Tuple

Point = Tuple[float, float]


def euclidean(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def zero(a: Point, b: Point) -> float:
    """h(n) = 0 turns A* into Dijkstra (handy for experiments)."""
    return 0.0
