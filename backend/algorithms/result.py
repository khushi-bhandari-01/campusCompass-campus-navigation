from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SearchResult:
    found: bool
    path: List[str]
    cost: Optional[float]
    explored: List[str]            # nodes in the order they were expanded (CLOSED)
    generated: List[str]           # nodes in the order they were first discovered
    heap_pushes: int = 0
    stale_pops: int = 0
    reopened: int = 0
    execution_time_ms: float = 0.0
    trace: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def nodes_explored(self) -> int:
        return len(self.explored)

    @property
    def nodes_generated(self) -> int:
        return len(self.generated)
