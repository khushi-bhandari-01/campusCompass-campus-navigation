from typing import Dict, List, Optional


def reconstruct_path(parent: Dict[str, Optional[str]], goal: str) -> List[str]:
    path: List[str] = []
    node: Optional[str] = goal
    guard = len(parent) + 1
    while node is not None and guard > 0:
        path.append(node)
        node = parent.get(node)
        guard -= 1
    path.reverse()
    return path
