"""Graph generators for tests and benchmarks. All weights are >= Euclidean distance,
so the Euclidean heuristic stays admissible and consistent."""
import math
import random
from typing import Dict, List, Tuple


def _empty(ids):
    return {i: [] for i in ids}


def _connect(adj, coords, a, b, factor):
    w = math.hypot(coords[a][0] - coords[b][0], coords[a][1] - coords[b][1]) * factor
    adj[a].append((b, w))
    adj[b].append((a, w))


def grid_graph(width: int, height: int, seed: int = 0, wall_prob: float = 0.0, spacing: float = 10.0):
    rng = random.Random(seed)
    coords = {f"{x},{y}": (x * spacing, y * spacing) for x in range(width) for y in range(height)}
    adj = _empty(coords)
    for x in range(width):
        for y in range(height):
            for dx, dy in ((1, 0), (0, 1)):
                nx, ny = x + dx, y + dy
                if nx < width and ny < height and rng.random() >= wall_prob:
                    _connect(adj, coords, f"{x},{y}", f"{nx},{ny}", rng.uniform(1.0, 2.0))
    return adj, coords


def geometric_graph(n: int, k: int = 4, seed: int = 0, size: float = 1000.0):
    rng = random.Random(seed)
    coords = {f"n{i}": (rng.uniform(0, size), rng.uniform(0, size)) for i in range(n)}
    adj = _empty(coords)
    ids = list(coords)
    seen = set()
    for a in ids:
        near = sorted(ids, key=lambda b: math.hypot(coords[a][0] - coords[b][0], coords[a][1] - coords[b][1]))[1:k + 1]
        for b in near:
            if (min(a, b), max(a, b)) not in seen:
                seen.add((min(a, b), max(a, b)))
                _connect(adj, coords, a, b, rng.uniform(1.0, 1.5))
    return adj, coords


def sample_pairs(nodes: List[str], count: int, seed: int = 1) -> List[Tuple[str, str]]:
    rng = random.Random(seed)
    return [(rng.choice(nodes), rng.choice(nodes)) for _ in range(count)]
