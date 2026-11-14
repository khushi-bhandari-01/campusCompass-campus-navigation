# Architecture

```
frontend/ (Vercel)                      backend/ (Render)
  NavigatorPage  -- fetch -->  main.py (FastAPI + CORS)
   |- Sidebar                    |- services/route_service.py  -> runs A*
   |- CampusMap (SVG)            |- services/graph_service.py  -> loads JSON, builds graph
   |- Controls / hook            |- algorithms/astar.py, priority_queue.py,
   |- AnalyticsPanel                heuristic.py, path_reconstruction.py, dijkstra.py (benchmark only)
   |- SearchProcess              |- map_data/campus_map.json
```

## Two synchronised representations of the map
Both come from `backend/map_data/campus_map.json`:
- **Visual layer** (`buildings`, `green_spaces`, `trees`, node coordinates, edges as drawn roads) is rendered as SVG by `CampusMap.jsx`.
- **Logical layer** (`nodes`, `edges` with `weight`) becomes an adjacency list in `graph_service.py` and is searched by A*.

Buildings are not graph nodes. Each building has an **entrance node** (type `entrance`) located on a road and linked to neighbouring road nodes; locations map to those entrance nodes (`locations[].node`).

## Request flow
1. Frontend loads `GET /api/map` and draws the campus.
2. User picks source and destination.
3. `POST /api/find-route` -> `route_service.find_route` resolves ids to nodes.
4. A* runs twice with identical results: once untraced (accurate timing), once with `record_trace=True` (animation data).
5. Response: route, coordinates, cost, explored/generated lists, trace, metrics.
6. `useTraceAnimation` reveals trace steps over time; `CampusMap` colours nodes (current, OPEN, CLOSED) and finally draws the route.

## Editing the campus
Add nodes/edges/buildings/locations in the JSON. Edge `weight` must be at least the Euclidean distance between its end nodes (use a factor of 1 or more), or the heuristic stops being admissible. A test (`test_edge_weights_are_not_below_euclidean_distance`) checks this.

## Configuration
- Frontend: `VITE_API_BASE_URL` (production). In development Vite proxies `/api` to `127.0.0.1:8000`.
- Backend: `ALLOWED_ORIGINS` (CORS), `PORT` (set by the host).
