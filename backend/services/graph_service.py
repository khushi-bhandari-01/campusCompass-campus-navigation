"""Loads campus_map.json and builds the weighted graph used by the search engine.

The JSON file is the single source of truth: the frontend draws it (visual layer)
and the backend searches it (logical layer). Edit the JSON to change the campus.
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple

DEFAULT_MAP_PATH = Path(__file__).resolve().parent.parent / "map_data" / "campus_map.json"


class CampusGraph:
    def __init__(self, path: Path = DEFAULT_MAP_PATH) -> None:
        with open(path, "r", encoding="utf-8") as fh:
            self.raw: dict = json.load(fh)
        self.nodes: Dict[str, dict] = {n["id"]: n for n in self.raw["nodes"]}
        self.locations: Dict[str, dict] = {l["id"]: l for l in self.raw["locations"]}
        self.coords: Dict[str, Tuple[float, float]] = {i: (n["x"], n["y"]) for i, n in self.nodes.items()}
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {i: [] for i in self.nodes}
        for e in self.raw["edges"]:
            a, b, w = e["source"], e["target"], float(e["weight"])
            self.adjacency[a].append((b, w))   # roads are two-way
            self.adjacency[b].append((a, w))
        self.meters_per_unit: float = self.raw["meta"].get("meters_per_unit", 1.0)

    def resolve(self, identifier: str) -> str:
        """Accept a location id (e.g. 'library') or a raw node id (e.g. 'J5')."""
        if identifier in self.locations:
            return self.locations[identifier]["node"]
        if identifier in self.nodes:
            return identifier
        raise KeyError(identifier)
