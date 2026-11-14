"""Benchmark A* against Dijkstra on identical graphs.

Run from the backend folder:   python -m benchmarks.run_benchmark
Reports: mean time, nodes explored/generated, cost, success rate, peak memory (tracemalloc),
and verifies that A* and Dijkstra always return the same optimal cost.
"""
import time
import tracemalloc

from algorithms.astar import astar
from algorithms.dijkstra import dijkstra
from benchmarks.generators import geometric_graph, grid_graph, sample_pairs
from services.graph_service import CampusGraph


def measure(fn, pairs):
    times, explored, generated, costs, ok = [], 0, 0, [], 0
    tracemalloc.start()
    for s, g in pairs:
        t = time.perf_counter()
        r = fn(s, g)
        times.append((time.perf_counter() - t) * 1000)
        explored += r.nodes_explored
        generated += r.nodes_generated
        costs.append(r.cost)
        ok += r.found
    peak = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    n = len(pairs)
    return dict(ms=sum(times) / n, explored=explored / n, generated=generated / n, ok=ok / n, peak_kb=peak, costs=costs)


def run(name, adj, coords, pairs):
    a = measure(lambda s, g: astar(adj, coords, s, g), pairs)
    d = measure(lambda s, g: dijkstra(adj, s, g), pairs)
    same = all((x is None and y is None) or (x is not None and y is not None and abs(x - y) < 1e-6)
               for x, y in zip(a["costs"], d["costs"]))
    print(f"{name:<22}{len(adj):>6} nodes | A*: {a['ms']:8.3f} ms  expl {a['explored']:8.1f}  gen {a['generated']:8.1f}"
          f"  mem {a['peak_kb']:8.1f} KB | Dijkstra: {d['ms']:8.3f} ms  expl {d['explored']:8.1f}  gen {d['generated']:8.1f}"
          f"  mem {d['peak_kb']:8.1f} KB | success {a['ok']*100:5.1f}% | costs equal: {same}")
    assert same, "A* returned a different cost from Dijkstra!"


def main():
    campus = CampusGraph()
    run("campus", campus.adjacency, campus.coords, sample_pairs(list(campus.adjacency), 100))
    for label, (adj, coords) in {
        "grid 20x20": grid_graph(20, 20, seed=1),
        "grid 60x60": grid_graph(60, 60, seed=2),
        "grid 40x40 w/ walls": grid_graph(40, 40, seed=3, wall_prob=0.35),
        "geometric 2000": geometric_graph(2000, seed=4),
    }.items():
        run(label, adj, coords, sample_pairs(list(adj), 50))
    print("All A* results matched the Dijkstra optimum.")


if __name__ == "__main__":
    main()
