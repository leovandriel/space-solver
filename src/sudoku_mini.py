# ruff: noqa: D100 D101 D102 D103 D105 D107

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from src.solver import solve
from src.space import PlanarSpace

if TYPE_CHECKING:
    from pathlib import Path

COUNT = 9
SUB = 3


class Table(PlanarSpace):
    def load(self: Table, text: str) -> None:
        for y, row in enumerate(text.split("\n")):
            for x, position in enumerate(row):
                if position != " ":
                    self.solve((x, y), int(position) - 1)

    def propagate(self: Table, index: tuple[int, int]) -> bool:  # type: ignore[override]
        x, y = index
        state = self.get((x, y)).state
        for xx in range(COUNT):
            if xx != x and not self.remove((xx, y), [state]):
                return False
        for yy in range(COUNT):
            if yy != y and not self.remove((x, yy), [state]):
                return False
        for xx in range(x // SUB * SUB, x // SUB * SUB + COUNT // SUB):
            for yy in range(
                y // SUB * SUB,
                y // SUB * SUB + COUNT // SUB,
            ):
                if xx != x and yy != y and not self.remove((xx, yy), [state]):
                    return False
        return True

    def __str__(self: Table) -> str:
        return "\n".join(
            "".join(str(i) if i is not None else " " for i in row)
            for row in self.matrix
        )


def run(filename: Path) -> None:
    table = Table(count=COUNT, size=(COUNT, COUNT))
    with filename.open() as f:
        table.load(f.read())
    solved = solve(table)
    sys.stderr.write(f"{'SOLVED' if solved else 'UNSOLVED'}\n{table}\n")
