from typing import Any, List, Tuple


class MinHeap:
    def __init__(self) -> None:
        self._data: List[Tuple[Any, int, Any]] = []
        self._counter = 0

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def push(self, key: Any, item: Any) -> None:
        self._data.append((key, self._counter, item))
        self._counter += 1
        self._sift_up(len(self._data) - 1)

    def peek(self) -> Tuple[Any, Any]:
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0][0], self._data[0][2]

    def pop(self) -> Tuple[Any, Any]:
        if not self._data:
            raise IndexError("pop from empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top[0], top[2]

    def _less(self, i: int, j: int) -> bool:
        return (self._data[i][0], self._data[i][1]) < (self._data[j][0], self._data[j][1])

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self._less(i, parent):
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self._data)
        while True:
            left, right, smallest = 2 * i + 1, 2 * i + 2, i
            if left < n and self._less(left, smallest):
                smallest = left
            if right < n and self._less(right, smallest):
                smallest = right
            if smallest == i:
                return
            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
            i = smallest
