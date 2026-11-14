# Project Overview

**PATHFINDER** is an interactive campus navigation system. A user clicks a start and a destination on a minimalist 2D campus map; the Python backend runs A* search and returns the optimal route plus a full trace of how the search proceeded; the browser draws the route and replays the search.

## Problem
Finding the shortest path between two places is a classic AI search problem. Blind searches (BFS, Dijkstra) explore in all directions. A* uses a heuristic to focus the search toward the goal.

## Goals
1. Implement A* from scratch (heap, OPEN/CLOSED, g/h/f, parents, reconstruction).
2. Visualise the real execution, not a fake animation.
3. Keep map data separate from code so the campus can be changed by editing JSON.
4. Verify optimality against Dijkstra on many graphs.

## The campus
Fictional "PATHFINDER Demo University", 1000 x 700 drawing units (1 unit is about 0.5 m).
- Gates: Main, North, East.
- Buildings: Library, Academic Block, Administration Block, Computer Science Department, Mechanical Department, Auditorium, Cafeteria, Sports Complex, Student Activity Centre, Parking Area, Medical Centre.
- 15 road junctions, building entrance nodes on the roads, 4 diagonal shortcut paths (cost x1.1), 3 green spaces.

## What is real vs. simulated
Everything shown is real: the route, costs, explored nodes, counts and timings all come from the backend. The only "playback" element is the timer that reveals recorded trace steps one by one.

## Folder map
`backend/` API + algorithms + tests + benchmarks, `frontend/` React app, `docs/` documentation. See ARCHITECTURE.md.
