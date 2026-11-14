# Algorithm Explanation (A* Search)

## Informed vs. uninformed search
Uninformed (blind) search such as BFS or Dijkstra uses only the problem definition. **Informed (heuristic) search** also uses problem-specific knowledge, a heuristic h(n), to decide which node looks most promising.

## What A* is
A* repeatedly expands the node in OPEN with the smallest

    f(n) = g(n) + h(n)

- **g(n)**: exact cost of the cheapest known path from the start to n.
- **h(n)**: estimated cost from n to the goal. Here: straight-line (Euclidean) distance.
- **f(n)**: estimated cost of the best path through n.

It is informed because h(n) steers the search toward the goal.

## Data structures (all in `backend/algorithms/`)
- **OPEN**: custom binary min-heap (`priority_queue.py`) keyed by `(f, h)`; ties are FIFO. Duplicate entries are allowed; outdated ones are skipped when popped (lazy decrease-key).
- **CLOSED**: a set of expanded nodes.
- **g_score / parent** dictionaries; `reconstruct_path` follows parents from goal to start.

## Pseudocode
```
push start with f = h(start)
while OPEN not empty:
    n = pop lowest f;  skip if stale/closed
    add n to CLOSED
    if n == goal: return reconstruct_path(goal)
    for each neighbour m with edge weight w:
        tentative = g(n) + w
        if m is new, or tentative < g(m):     (re-open if m was closed)
            g(m) = tentative; parent(m) = n; push m with f = g(m) + h(m)
return failure
```

## Admissibility and consistency
- **Admissible**: h(n) never overestimates the true remaining cost. Straight-line distance cannot exceed the length of any path, and every edge weight is Euclidean length x factor (factor >= 1).
- **Consistent (monotone)**: h(a) <= w(a,b) + h(b) for every edge. This follows from the triangle inequality, and it guarantees the first time a node is expanded its g is already optimal, so no node is ever re-opened. The tests assert `reopened == 0` on the campus graph.
- Consequence: A* returns an **optimal** path. The tests compare against Dijkstra on every node pair of the campus and on random grid and geometric graphs.

## Complexity
- Worst case: time and space O(b^d) in the search tree (branching factor b, depth d).
- On a finite graph with a binary heap and consistent heuristic: each node is expanded at most once, so O((V + E) log V) time and O(V) space. The benchmark shows A* expanding about half as many nodes as Dijkstra on grids and about a third on large random geometric graphs; on the tiny campus graph the time difference is negligible.

## Advantages and limitations
+ Optimal with an admissible heuristic; usually far fewer expansions than Dijkstra; simple to visualise.
- Memory grows with the frontier; quality depends on the heuristic; with h = 0 it degrades to Dijkstra; needs coordinates (or another heuristic source).

## How the app visualises it
Each expanded node produces one trace step: current node, g, h, f, parent, neighbours with the action taken (added, improved, skipped), and a snapshot of OPEN. The frontend replays exactly these steps.
