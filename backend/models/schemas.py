"""Pydantic request/response models."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    source: str = Field(..., min_length=1, description="Location id (e.g. 'library') or node id (e.g. 'J5')")
    destination: str = Field(..., min_length=1)


class Metrics(BaseModel):
    execution_time_ms: float
    nodes_explored: int
    nodes_generated: int
    path_nodes: int
    heap_pushes: int
    stale_pops: int
    reopened: int


class RouteResponse(BaseModel):
    success: bool
    status: str
    message: str
    source_node: str
    destination_node: str
    route: List[str]
    route_coordinates: List[Dict[str, Any]]
    total_cost: Optional[float]
    distance_m: Optional[float]
    explored: List[str]
    generated: List[str]
    trace: List[Dict[str, Any]]
    metrics: Metrics
