# ruff: noqa: D100 D101 D102 D103 D105 D107

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from src.pygame import pygame
from src.solver import solve
from src.space import PlanarSpace
from src.utils import await_key, flush_surface, setup_surface

if TYPE_CHECKING:
    from pathlib import Path

COUNT = 9
SUB = 3
DRAW_SIZE = (500, 500)
FILL_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
FRAME_DELAY = 0.001


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

    def is_valid(self: Table) -> bool:  # noqa: C901 PLR0912
        correct = set(range(9))
        for y in range(COUNT):
            for x in range(COUNT):
                if not self.get((x, y)).is_solved:
                    return False
        for y in range(COUNT):
            row = set()
            for x in range(COUNT):
                row.add(self.get((x, y)).state)
            if row != correct:
                return False
        for x in range(COUNT):
            col = set()
            for y in range(COUNT):
                col.add(self.get((x, y)).state)
            if col != correct:
                return False
        for x in range(COUNT // SUB):
            for y in range(COUNT // SUB):
                block = set()
                for xx in range(COUNT // SUB):
                    for yy in range(COUNT // SUB):
                        block.add(self.get((x * SUB + xx, y * SUB + yy)).state)
                if block != correct:
                    return False
        return True

    def draw(
        self: Table,
        surface: pygame.Surface,
    ) -> None:
        pygame.draw.rect(
            surface,
            FILL_COLOR,
            (0, 0, DRAW_SIZE[0], DRAW_SIZE[1]),
        )
        min_size = min(DRAW_SIZE) // COUNT
        small = pygame.font.SysFont("Arial", min_size // 4)
        large = pygame.font.SysFont("Arial", min_size // 4 * 3)
        step = ((DRAW_SIZE[0] - 1) / COUNT, (DRAW_SIZE[1] - 1) / COUNT)
        for i in range(COUNT + 1):
            width = SUB if i % SUB == 0 else 1
            pygame.draw.line(
                surface,
                LINE_COLOR,
                (i * step[0], 0),
                (i * step[0], DRAW_SIZE[1]),
                width,
            )
            pygame.draw.line(
                surface,
                LINE_COLOR,
                (0, i * step[1]),
                (DRAW_SIZE[0], i * step[1]),
                width,
            )
        for y in range(COUNT):
            for x in range(COUNT):
                postion = self.get((x, y))
                if postion.is_solved:
                    text = large.render(
                        str(postion),
                        True,  # noqa: FBT003
                        TEXT_COLOR,
                    )
                    surface.blit(
                        text,
                        (x * step[0] + step[0] / 3, y * step[1] + step[1] / 8),
                    )
                else:
                    for yy in range(COUNT // SUB):
                        for xx in range(COUNT // SUB):
                            index = yy * SUB + xx
                            if self.get((x, y)).has(index):
                                text = small.render(
                                    str(index + 1),
                                    True,  # noqa: FBT003
                                    TEXT_COLOR,
                                )
                                surface.blit(
                                    text,
                                    (
                                        x * step[0] + xx * step[0] // SUB + step[1] / 8,
                                        y * step[1]
                                        + yy * step[1] // SUB
                                        + step[1] / 20,
                                    ),
                                )


def draw_wait(table: Table, window: pygame.Surface, surface: pygame.Surface) -> None:
    table.draw(surface)
    flush_surface(window, surface)
    await_key(seconds=FRAME_DELAY)


def run(filename: Path | None) -> None:
    random.seed(0)
    window, surface = setup_surface("Solve Sudoku", DRAW_SIZE)
    table = Table(count=COUNT, size=(COUNT, COUNT))
    if filename is not None:
        with filename.open() as f:
            table.load(f.read())
    solved = solve(
        table,
        lambda t: draw_wait(t, window, surface),  # type: ignore[arg-type]
    )
    valid = table.is_valid()
    pygame.display.set_caption(
        ("SOLVED" if valid and solved else "UNSOLVED" if valid else "INVALID")
        + " (ESC to exit)",
    )
    draw_wait(table, window, surface)
    await_key()
