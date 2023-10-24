"""Solver for spaces."""

from __future__ import annotations

import random
from typing import Callable

from src.space import Space, SpaceIndex

NOT_FOUND = object()
Callback = Callable[[Space], None]


def propagate_queue(space: Space) -> bool:
    """Propagate the solved state of a position into dependent positions."""
    while space.queue:
        index = space.queue.pop(0)
        if not space.propagate(index):
            return False
    return True


    """Return the index of the position with the lowest entropy."""
def min_count(space: Space) -> SpaceIndex:
    minimum = None
    indices = []
    for index, position in space.positions:
        count = position.count
        if (minimum is None or minimum >= count) and count > 1:
            if minimum == count:
                indices.append(index)
            else:
                minimum = count
                indices = [index]
    return random.choice(indices) if len(indices) > 0 else NOT_FOUND  # noqa: S311


def solve_index(
    space: Space,
    index: SpaceIndex,
    callback: Callback | None = None,
) -> bool:
    """Set the position state at the given index to the given state."""
    states = space.get(index).states
    for state in states:
        copy = space.copy()
        copy.solve(index, state)
        if solve(copy, callback):
            space.assign(copy)
            return True
    return False


def solve(space: Space, callback: Callback | None = None) -> bool:
    """Solve all positions in the space into a valid state."""
    if callback is not None:
        callback(space)
    if not propagate_queue(space):
        return False
    index = min_count(space)
    return index == NOT_FOUND or solve_index(space, index, callback)
