import random

import pytest

from algorithms.priority_queue import MinHeap


def test_pops_in_sorted_order():
    rng = random.Random(1)
    values = [rng.random() for _ in range(500)]
    h = MinHeap()
    for v in values:
        h.push((v,), v)
    out = [h.pop()[1] for _ in range(len(values))]
    assert out == sorted(values)
    assert h.is_empty()


def test_ties_are_fifo():
    h = MinHeap()
    for name in "abc":
        h.push((1,), name)
    assert [h.pop()[1] for _ in range(3)] == ["a", "b", "c"]


def test_peek_and_empty_errors():
    h = MinHeap()
    with pytest.raises(IndexError):
        h.pop()
    with pytest.raises(IndexError):
        h.peek()
    h.push((2,), "x")
    h.push((1,), "y")
    assert h.peek()[1] == "y" and len(h) == 2
