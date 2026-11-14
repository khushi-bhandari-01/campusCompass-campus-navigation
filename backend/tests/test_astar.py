import math

import pytest

from algorithms.astar import astar
from algorithms.dijkstra import dijkstra
from benchmarks.generators import geometric_graph, grid_graph, sample_pairs
from services.graph_service import CampusGraph


def make(edges, coords):
    adj = {n: [] for n in coords}
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    return adj


def path_cost(adj, path):
    total = 0.0
    for a, b in zip(path, path[1:]):
        total += next(w for n, w in adj[a] if n == b)   # raises StopIteration if edge missing
    return total


COORDS = {"A": (0, 0), "B": (10, 0), "C": (10, 10), "D": (0, 10), "Z": (100, 100)}


def test_small_graph_shortest_path():
    adj = make([("A", "B", 10), ("B", "C", 10), ("A", "D", 10), ("D", "C", 15)], COORDS)
    r = astar(adj, COORDS, "A", "C")
    assert r.found and r.path == ["A", "B", "C"] and r.cost == pytest.approx(20)


def test_multiple_alternative_routes_picks_cheapest():
    # Direct edge is long (weight 30, still >= distance); detour is cheaper overall.
    adj = make([("A", "C", 30), ("A", "B", 10), ("B", "C", 10)], COORDS)
    r = astar(adj, COORDS, "A", "C")
    assert r.path == ["A", "B", "C"] and r.cost == pytest.approx(20)


def test_different_edge_weights_change_route():
    adj = make([("A", "B", 40), ("B", "C", 10), ("A", "D", 12), ("D", "C", 14)], COORDS)
    assert astar(adj, COORDS, "A", "C").path == ["A", "D", "C"]


def test_unreachable_destination():
    adj = make([("A", "B", 10)], COORDS)
    r = astar(adj, COORDS, "A", "Z")
    assert not r.found and r.path == [] and r.cost is None


def test_source_equals_destination():
    adj = make([("A", "B", 10)], COORDS)
    r = astar(adj, COORDS, "A", "A")
    assert r.found and r.path == ["A"] and r.cost == 0


def test_unknown_node_raises():
    adj = make([("A", "B", 10)], COORDS)
    with pytest.raises(KeyError):
        astar(adj, COORDS, "A", "nope")


def test_trace_is_consistent_with_search():
    adj = make([("A", "B", 10), ("B", "C", 10), ("A", "D", 10), ("D", "C", 15)], COORDS)
    r = astar(adj, COORDS, "A", "C", record_trace=True)
    assert [s["current"] for s in r.trace] == r.explored
    assert r.trace[-1]["goal_reached"] and r.trace[0]["current"] == "A"
    for s in r.trace:
        assert s["f"] == pytest.approx(s["g"] + s["h"], abs=1e-3)


def test_campus_graph_matches_dijkstra_for_every_pair():
    campus = CampusGraph()
    nodes = list(campus.adjacency)
    for s in nodes:
        for g in nodes:
            a = astar(campus.adjacency, campus.coords, s, g)
            d = dijkstra(campus.adjacency, s, g)
            assert a.found and d.found
            assert a.cost == pytest.approx(d.cost, abs=1e-6)
            assert path_cost(campus.adjacency, a.path) == pytest.approx(a.cost, abs=1e-6)
            assert a.path[0] == s and a.path[-1] == g
            assert a.reopened == 0   # consistent heuristic => no re-opening


@pytest.mark.parametrize("builder", [
    lambda: grid_graph(15, 15, seed=1),
    lambda: grid_graph(30, 30, seed=2, wall_prob=0.4),     # contains unreachable pairs
    lambda: geometric_graph(600, seed=3),                   # "large graph"
])
def test_matches_dijkstra_on_random_graphs(builder):
    adj, coords = builder()
    for s, g in sample_pairs(list(adj), 60):
        a, d = astar(adj, coords, s, g), dijkstra(adj, s, g)
        assert a.found == d.found
        if a.found:
            assert a.cost == pytest.approx(d.cost, abs=1e-6)
            assert path_cost(adj, a.path) == pytest.approx(a.cost, abs=1e-6)


def test_astar_explores_fewer_nodes_than_dijkstra_on_open_grid():
    adj, coords = grid_graph(40, 40, seed=5)
    a, d = astar(adj, coords, "0,0", "39,39"), dijkstra(adj, "0,0", "39,39")
    assert a.cost == pytest.approx(d.cost, abs=1e-6)
    assert a.nodes_explored < d.nodes_explored


def test_edge_weights_are_not_below_euclidean_distance():
    campus = CampusGraph()
    for a, nbrs in campus.adjacency.items():
        for b, w in nbrs:
            d = math.hypot(campus.coords[a][0] - campus.coords[b][0], campus.coords[a][1] - campus.coords[b][1])
            assert w >= d - 1e-9
