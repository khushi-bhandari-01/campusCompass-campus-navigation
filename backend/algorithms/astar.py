"""A* search implemented from scratch.

    f(n) = g(n) + h(n)

g(n): cost of the best known path start -> n.   h(n): heuristic estimate n -> goal.
OPEN   = custom binary min-heap ordered by (f, h); duplicates are allowed and stale
         entries are discarded when popped (lazy decrease-key).
CLOSED = set of expanded nodes. With a consistent heuristic a closed node is never
         improved; the code still re-opens a node if a cheaper path appears, so it
         also stays correct with an inconsistent heuristic.
"""
import time
from typing import Callable, Dict, List, Optional, Tuple

from .heuristic import euclidean
from .path_reconstruction import reconstruct_path
from .priority_queue import MinHeap
from .result import SearchResult

EPS = 1e-12
Adjacency = Dict[str, List[Tuple[str, float]]]
Coords = Dict[str, Tuple[float, float]]


def astar(adjacency: Adjacency, coords: Coords, start: str, goal: str,
          heuristic: Callable = euclidean, record_trace: bool = False) -> SearchResult:
    if start not in adjacency:
        raise KeyError(f"Unknown start node: {start}")
    if goal not in adjacency:
        raise KeyError(f"Unknown goal node: {goal}")

    t0 = time.perf_counter()
    goal_xy = coords[goal]

    def h(n: str) -> float:
        return heuristic(coords[n], goal_xy)

    g_score: Dict[str, float] = {start: 0.0}
    parent: Dict[str, Optional[str]] = {start: None}
    closed: set = set()
    open_nodes: Dict[str, float] = {start: 0.0}   # nodes with a live OPEN entry -> g
    heap = MinHeap()
    h0 = h(start)
    heap.push((h0, h0), (start, 0.0))

    generated = [start]
    explored: List[str] = []
    trace: List[dict] = []
    pushes, stale, reopened, found = 1, 0, 0, False

    while not heap.is_empty():
        _, (node, g_val) = heap.pop()
        if node in closed or g_val > g_score[node] + EPS:
            stale += 1                       # outdated duplicate entry
            continue
        open_nodes.pop(node, None)
        closed.add(node)
        explored.append(node)
        h_n = h(node)

        step = None
        if record_trace:
            step = {"step": len(trace) + 1, "current": node, "g": round(g_val, 4), "h": round(h_n, 4),
                    "f": round(g_val + h_n, 4), "parent": parent[node], "goal_reached": node == goal,
                    "neighbors": [], "open": [], "closed_count": len(closed)}

        if node == goal:
            found = True
            if step is not None:
                step["open"] = _open_snapshot(open_nodes, h)
                trace.append(step)
            break

        for nbr, weight in adjacency[node]:
            tentative = g_val + weight
            if nbr in closed:
                if tentative < g_score[nbr] - EPS:
                    closed.discard(nbr)
                    reopened += 1
                    action = "reopened"
                else:
                    if step is not None:
                        step["neighbors"].append(_nb(nbr, g_score[nbr], h(nbr), "skipped_closed"))
                    continue
            elif nbr not in g_score:
                action = "added"
                generated.append(nbr)
            elif tentative < g_score[nbr] - EPS:
                action = "improved"
            else:
                if step is not None:
                    step["neighbors"].append(_nb(nbr, g_score[nbr], h(nbr), "skipped_worse"))
                continue
            g_score[nbr] = tentative
            parent[nbr] = node
            h_v = h(nbr)
            heap.push((tentative + h_v, h_v), (nbr, tentative))
            open_nodes[nbr] = tentative
            pushes += 1
            if step is not None:
                step["neighbors"].append(_nb(nbr, tentative, h_v, action))

        if step is not None:
            step["open"] = _open_snapshot(open_nodes, h)
            trace.append(step)

    elapsed = (time.perf_counter() - t0) * 1000
    if found:
        return SearchResult(True, reconstruct_path(parent, goal), g_score[goal], explored, generated,
                            pushes, stale, reopened, elapsed, trace)
    return SearchResult(False, [], None, explored, generated, pushes, stale, reopened, elapsed, trace)


def _nb(node: str, g: float, h_v: float, action: str) -> dict:
    return {"id": node, "g": round(g, 4), "h": round(h_v, 4), "f": round(g + h_v, 4), "action": action}


def _open_snapshot(open_nodes: Dict[str, float], h: Callable) -> List[dict]:
    rows = [{"id": n, "g": round(g, 4), "h": round(h(n), 4), "f": round(g + h(n), 4)} for n, g in open_nodes.items()]
    return sorted(rows, key=lambda r: (r["f"], r["h"]))
