"""Glue between the HTTP layer and the A* engine."""
from algorithms.astar import astar
from .graph_service import CampusGraph


def find_route(graph: CampusGraph, source: str, destination: str) -> dict:
    start, goal = graph.resolve(source), graph.resolve(destination)

    # Pass 1: timed run WITHOUT trace recording, so the reported time is the search itself.
    timed = astar(graph.adjacency, graph.coords, start, goal, record_trace=False)
    # Pass 2: identical deterministic search that records the step-by-step trace for animation.
    traced = astar(graph.adjacency, graph.coords, start, goal, record_trace=True)

    if traced.found:
        status = "found"
        message = ("Source and destination are the same place." if start == goal
                   else "Optimal route found with A* search.")
    else:
        status = "no_route"
        message = "No walkable route exists between these two locations."

    return {
        "success": traced.found,
        "status": status,
        "message": message,
        "source_node": start,
        "destination_node": goal,
        "route": traced.path,
        "route_coordinates": [{"id": n, "x": graph.coords[n][0], "y": graph.coords[n][1]} for n in traced.path],
        "total_cost": traced.cost,
        "distance_m": None if traced.cost is None else round(traced.cost * graph.meters_per_unit, 2),
        "explored": traced.explored,
        "generated": traced.generated,
        "trace": traced.trace,
        "metrics": {
            "execution_time_ms": round(timed.execution_time_ms, 4),
            "nodes_explored": traced.nodes_explored,
            "nodes_generated": traced.nodes_generated,
            "path_nodes": len(traced.path),
            "heap_pushes": traced.heap_pushes,
            "stale_pops": traced.stale_pops,
            "reopened": traced.reopened,
        },
    }
