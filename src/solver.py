"""Solver for spaces.

The solver uses a combination of constraint propagation and random assignment
with backgracking if constraint propagation fails.
"""

from __future__ import annotations

import random
from typing import Callable

from src.space import Space, SpaceIndex

NOT_FOUND = object()
Callback = Callable[[Space], None]


def propagate_queue(space: Space) -> bool:
    """Propagate all solved states listed in the queue into dependent positions."""
    while space.queue:
        index = space.queue.pop(0)
        if not space.propagate(index):
            return False
    return True


def ensure_edge(space: Space) -> None:
    """Ensure that at least one index is considered edge to start solving.

    Space keeps track of an egde set which is used as candidates for unsolved
    positions. In some cases, e.g. at the start, this set can be empty. To kick
    off the solver, randomly select an egde element.
    """
    if not space.edge:
        indices = [index for index, _ in space.positions]
        space.edge.add(random.choice(indices))


def select_position(space: Space) -> SpaceIndex:
    """Return unsolved position with the lowest number of states.

    This position is used to continue the solving process, by marking it as
    solved and recursively solving from there, backtracking if a conflict
    arises..
    """
    ensure_edge(space)
    minimum = None
    indices = []
    for index in space.edge:
        count = space.get(index).count
        if (minimum is None or minimum >= count) and count > 1:
            if minimum == count:
                indices.append(index)
            else:
                minimum = count
                indices = [index]
    return random.choice(indices) if indices else NOT_FOUND


def solve_index(
    space: Space,
    index: SpaceIndex,
    callback: Callback | None = None,
) -> bool:
    """Set the state for position at index and solve recursively.

    After all propagations have completed there can still be unsolved positions.
    To address this, we duplicate the space, assume a solution at this given
    index, and try to solving from there. If we run into a conflict, we discard
    the space.

    Returns True if the space is solved, False otherwise.
    """
    states = space.get(index).states
    for state in states:
        copy = space.copy()
        copy.solve(index, state)
        if solve_space(copy, callback):
            space.assign(copy)
            return True
    return False


def solve_space(space: Space, callback: Callback | None = None) -> bool:
    """Solve all positions in the space recursively.

    First propagate all solved positions listed in the queue. Then find the
    unsolved position with minimal number of states and assign a random state to
    recursively solve from.

    Returns True if the space is solved, False otherwise.
    """
    if callback is not None:
        callback(space)
    if not propagate_queue(space):
        return False
    index = select_position(space)
    return index == NOT_FOUND or solve_index(space, index, callback)
