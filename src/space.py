"""Various space classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Protocol, cast

from src.position import DiscretePosition, Position, PositionState


class SpaceIndex(Protocol):
    """An index of a position in a space."""


class Space(ABC):
    """An abstract space."""

    queue: list[SpaceIndex]
    edge: set[SpaceIndex]

    @abstractmethod
    def copy(self: Space) -> Space:
        """Return a copy of this space."""

    @abstractmethod
    def assign(self: Space, source: Space) -> None:
        """Assign the given space to this space."""

    @property
    @abstractmethod
    def positions(self: Space) -> Iterator[tuple[SpaceIndex, Position]]:
        """Iterator over all index-positions pairs in the space."""

    @abstractmethod
    def get(self: Space, index: SpaceIndex) -> Position:
        """Return the position at the given index."""

    @abstractmethod
    def propagate(self: Space, index: SpaceIndex) -> bool:
        """Propagate the solved state of a position into dependent positions.

        This function defines how the space is structured, by defining how
        reduction in states in one position impacts states in other positions
        """

    def solve(self: Space, index: SpaceIndex, state: PositionState) -> bool:
        """Set a single state to the position at the given index.

        By setting to a single state, we can propagate into dependent positions,
        further reducing state
        """
        position = self.get(index)
        position.solve(state)
        if not position.is_solved:
            return False
        self.queue.append(index)
        self.edge.discard(index)
        return True

    def remove(self: Space, index: SpaceIndex, states: Iterable[PositionState]) -> bool:
        """Remove the given states from the position at the given index.

        If this results in a single state, we propagate into dependent positions.
        """
        position = self.get(index)
        for state in states:
            if not position.has(state):
                continue
            if position.is_solved:
                return False
            position.remove([state])
            if position.is_solved:
                self.queue.append(index)
                self.edge.remove(index)
            else:
                self.edge.add(index)
        return True


class PlanarSpace(Space):
    """A 2D space."""

    matrix: list[list[DiscretePosition]]

    def __init__(  # noqa: PLR0913
        self: PlanarSpace,
        matrix: list[list[DiscretePosition]] | None = None,
        queue: list[SpaceIndex] | None = None,
        edge: set[SpaceIndex] | None = None,
        count: int = 0,
        size: tuple[int, int] = (0, 0),
    ) -> None:
        """Create a space with the given matrix or size."""
        self.matrix = (
            [
                [DiscretePosition(size=count) for x in range(size[0])]
                for y in range(size[1])
            ]
            if matrix is None
            else matrix
        )
        self.queue = [] if queue is None else queue
        self.edge = set() if edge is None else edge

    def copy(self: PlanarSpace) -> PlanarSpace:
        """Return a deep copy of this space."""
        return self.__class__(
            matrix=[[position.copy() for position in row] for row in self.matrix],
            queue=self.queue.copy(),
            edge=self.edge.copy(),
        )

    def assign(self: PlanarSpace, right: Space) -> None:
        """Assign the given space to this space."""
        if not isinstance(right, PlanarSpace):
            raise TypeError
        self.matrix = right.matrix
        self.queue = right.queue
        self.edge = right.edge

    @property
    def positions(self: PlanarSpace) -> Iterator[tuple[tuple[int, int], Position]]:
        """Iterator over all index-positions pairs in the space."""
        return (
            ((x, y), position)
            for y, row in enumerate(self.matrix)
            for x, position in enumerate(row)
        )

    def get(self: PlanarSpace, index: SpaceIndex) -> DiscretePosition:
        """Return the position at the given index."""
        x, y = cast(tuple[int, int], index)
        return self.matrix[y][x]
