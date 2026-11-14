"""Dijkstra's algorithm: benchmark baseline ONLY (the navigation engine uses A*)."""
import time
from typing import Dict

from .astar import EPS, Adjacency
from .path_reconstruction import reconstruct_path
from .priority_queue import MinHeap
from .result import SearchResult


def dijkstra(adjacency: Adjacency, start: str, goal: str) -> SearchResult:
    if start not in adjacency or goal not in adjacency:
        raise KeyError("Unknown start or goal node")
    t0 = time.perf_counter()
    dist: Dict[str, float] = {start: 0.0}
    parent: Dict[str, object] = {start: None}
    closed: set = set()
    heap = MinHeap()
    heap.push((0.0,), (start, 0.0))
    generated, explored, pushes, stale, found = [start], [], 1, 0, False
    while not heap.is_empty():
        _, (node, d) = heap.pop()
        if node in closed or d > dist[node] + EPS:
            stale += 1
            continue
        closed.add(node)
        explored.append(node)
        if node == goal:
            found = True
            break
        for nbr, w in adjacency[node]:
            nd = d + w
            if nbr not in dist:
                generated.append(nbr)
            elif nd >= dist[nbr] - EPS:
                continue
            dist[nbr] = nd
            parent[nbr] = node
            heap.push((nd,), (nbr, nd))
            pushes += 1
    ms = (time.perf_counter() - t0) * 1000
    if found:
        return SearchResult(True, reconstruct_path(parent, goal), dist[goal], explored, generated, pushes, stale, 0, ms)
    return SearchResult(False, [], None, explored, generated, pushes, stale, 0, ms)
