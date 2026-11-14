# API Documentation

Base URL: `http://127.0.0.1:8000` locally. Interactive docs: `/docs` (Swagger) and `/redoc`.

## GET /api/health
`{"status": "ok"}`

## GET /api/map
Returns the whole campus JSON: `meta`, `nodes`, `edges`, `locations`, `buildings`, `green_spaces`, `trees`.

## GET /api/locations
List of `{id, name, type, node, x, y}` for the 14 selectable gates and buildings.

## POST /api/find-route
Request:
```json
{ "source": "main_gate", "destination": "auditorium" }
```
`source`/`destination` accept a location id (`library`) or a node id (`J5`).

Response (abridged):
```json
{
  "success": true,
  "status": "found",
  "message": "Optimal route found with A* search.",
  "source_node": "G_MAIN", "destination_node": "E_AUD",
  "route": ["G_MAIN", "J2", "J6", "E_CS", "J7", "J11", "E_AUD"],
  "route_coordinates": [{"id": "G_MAIN", "x": 500, "y": 680}],
  "total_cost": 810.0, "distance_m": 405.0,
  "explored": ["G_MAIN", "J2"], "generated": ["G_MAIN", "J2"],
  "trace": [{
    "step": 1, "current": "G_MAIN", "g": 0.0, "h": 595.4, "f": 595.4, "parent": null,
    "goal_reached": false, "closed_count": 1,
    "neighbors": [{"id": "J2", "g": 120.0, "h": 494.1, "f": 614.1, "action": "added"}],
    "open": [{"id": "J2", "g": 120.0, "h": 494.1, "f": 614.1}]
  }],
  "metrics": {"execution_time_ms": 0.08, "nodes_explored": 10, "nodes_generated": 16,
              "path_nodes": 7, "heap_pushes": 16, "stale_pops": 0, "reopened": 0}
}
```
- Neighbour `action` values: `added`, `improved`, `reopened`, `skipped_closed`, `skipped_worse`.
- No route: `success: false`, `status: "no_route"`, empty `route`, `total_cost: null`.
- Same source and destination: success with a one-node route and cost 0.
- Errors: `404` unknown location, `422` invalid body.
- `execution_time_ms` is measured on an untraced run of the search; the trace comes from an identical second run.

## POST /api/reset
`{"status": "ok", "message": "Search state cleared."}` The API is stateless; this is an acknowledgement endpoint.

## CORS
Set `ALLOWED_ORIGINS` (comma separated) on the backend, for example `https://my-app.vercel.app`.
