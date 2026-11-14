# Viva Preparation

## 30-second summary
PATHFINDER finds the optimal walking route on a campus graph using A* search written from scratch in Python. The browser replays the real search trace so you can see why each node was expanded.

## Questions and answers
**1. What is informed search?** Search that uses extra knowledge about the problem, a heuristic h(n), to guide exploration, unlike blind search (BFS, Dijkstra).

**2. What is A*?** A best-first graph search that expands the node with the lowest f(n) = g(n) + h(n); it is complete and optimal when h is admissible (and consistent on graphs).

**3. Why is A* informed?** Because h(n) injects knowledge (distance to goal) that biases the search toward the goal. With h = 0 it becomes Dijkstra.

**4. What do g, h and f mean?** g is the exact cost from the start; h is the estimated cost to the goal; f is the estimated total cost through the node.

**5. Which heuristic did you use and why?** Euclidean distance between node coordinates. Every edge weight is at least the straight-line distance between its endpoints, so it never overestimates.

**6. What is admissibility?** h(n) <= true cheapest cost from n to the goal for all n. It guarantees A* does not skip the optimal path.

**7. What is consistency?** h(a) <= w(a,b) + h(b) for each edge (the triangle inequality). It implies admissibility and means a node's g is optimal when first expanded, so CLOSED nodes are never re-opened.

**8. Why did you add a "shortcut" factor of 1.1?** To show that weights can differ from pure distance (e.g. rougher paths) while staying >= distance, keeping the heuristic valid. A test checks this for all edges.

**9. Explain OPEN and CLOSED.** OPEN holds discovered-but-unexpanded nodes (a min-heap by f). CLOSED holds expanded nodes. We pop the best from OPEN, move it to CLOSED, and push or update its neighbours.

**10. How do you handle a node reached by a cheaper path later?** The heap has no decrease-key, so we push a duplicate with the better g and skip outdated entries when popped (lazy deletion). The code also re-opens closed nodes if needed (never happens with consistent h).

**11. How did you build the priority queue?** A custom array-based binary min-heap with sift-up and sift-down; push and pop are O(log n). A counter breaks ties first-in-first-out.

**12. Time and space complexity?** Worst case O(b^d). On our graph with a binary heap and consistent h, each node is expanded once: O((V + E) log V) time, O(V) space.

**13. How did you verify optimality?** 21 automated tests: A* vs Dijkstra on all node pairs of the campus, on random grids (including blocked ones) and a 600-node geometric graph; path costs are recomputed edge by edge.

**14. When does A* beat Dijkstra? When not?** It expands fewer nodes when the heuristic is informative (benchmarks: about 2x fewer on grids, about 3x fewer on large random graphs). On a 29-node graph the difference is negligible, and with a useless heuristic it is no better.

**15. What happens if there is no route?** The OPEN list empties; the engine returns `found = false`, empty path and `null` cost; the UI shows "No route exists".

**16. Is the animation faked?** No. The backend records one trace step per expansion (current node, g/h/f, neighbours, OPEN snapshot). The frontend only replays those steps on a timer.

**17. Why separate frontend and backend hosting?** Vercel serves static files; the FastAPI server needs a Python process, hosted on Render. CORS lets the Vercel origin call the API.

**18. Limitations / future work?** Fictional map; free-tier cold starts; no live traffic or accessibility costs; possible extensions: one-way paths, indoor routing, multi-stop routes, weighted preferences, JPS or bidirectional search.

## Demo script
1. Show the map; click Main Gate then Auditorium. 2. Press Find route; point out OPEN (blue rings) and CLOSED (amber). 3. Pause on a step; read f = g + h and the OPEN table. 4. Finish: blue route, analytics. 5. Run `python -m benchmarks.run_benchmark` to show A* vs Dijkstra.
