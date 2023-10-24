"""Various position classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Protocol


class PositionState(Protocol):
    """A single state in a position."""


class Position(ABC):
    """A position in a space."""

    @property
    @abstractmethod
    def count(self: Position) -> float:
        """Number of states this position could be in."""

    @property
    @abstractmethod
    def is_solved(self: Position) -> bool:
        """True if can only be in one state."""

    @abstractmethod
    def has(self: Position, state: PositionState) -> bool:
        """Return true if can be in the given state."""

    @abstractmethod
    def remove(self: Position, states: Iterable[PositionState]) -> None:
        """Remove the given states from the position."""

    @abstractmethod
    def solve(self: Position, state: PositionState) -> None:
        """Remove all but one state from the position."""

    @property
    @abstractmethod
    def state(self: Position) -> PositionState:
        """Single state, assuming solved."""

    @property
    @abstractmethod
    def states(self: Position) -> Iterator[PositionState]:
        """All possible states."""


class DiscretePosition(Position):
    """A position represented by a list of booleans."""

    vector: list[bool]

    def __init__(
        self: DiscretePosition,
        vector: list[bool] | None = None,
        size: int = 0,
    ) -> None:
        """Create space with given size or internal vector."""
        self.vector = [True for i in range(size)] if vector is None else vector

    def copy(self: DiscretePosition) -> DiscretePosition:
        """Return a deep copy of this position."""
        return DiscretePosition(vector=self.vector.copy())

    @property
    def count(self: DiscretePosition) -> float:
        """Number of states this position could be in."""
        return self.vector.count(True)

    @property
    def is_solved(self: DiscretePosition) -> bool:
        """True if can only be in one state."""
        return self.vector.count(True) == 1

    def has(self: DiscretePosition, state: int) -> bool:  # type: ignore[override]
        """Return true if can be in the given state."""
        return self.vector[state]

    def remove(self: DiscretePosition, states: Iterable[int]) -> None:  # type: ignore[override]
        """Remove the given states from the position."""
        for state in states:
            self.vector[state] = False

    def solve(self: DiscretePosition, state: int) -> None:  # type: ignore[override]
        """Remove all but one state from the position."""
        for i, s in enumerate(self.vector):
            self.vector[i] = s and i == state

    @property
    def state(self: DiscretePosition) -> int:
        """Single state, assuming solved."""
        return self.vector.index(True)

    @property
    def states(self: DiscretePosition) -> Iterator[int]:
        """All possible states."""
        return (i for i, s in enumerate(self.vector) if s)

    def __str__(self: DiscretePosition) -> str:
        """Return a string representation of this position."""
        return str(self.vector.index(True) + 1) if self.is_solved else " "
