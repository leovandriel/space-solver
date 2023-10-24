# ruff: noqa: D100 D101 D102 D103 D105 D107

from __future__ import annotations

import math
import random

from src.pygame import pygame
from src.solver import solve
from src.space import PlanarSpace
from src.utils import await_key, flush_surface, setup_surface

GRID_SIZE = 25
STATE_COUNT = 4
FRAME_DELAY = 0.01
DRAW_SIZE = (1000, 1000)
DRAW_SCALE = 2
FILL_COLOR = (255, 255, 255)
STATE_COLOR = (128, 128, 128)
LINE_COLOR = (0, 0, 0)
EDGE_COLOR = (255, 128, 0)
LINE_WIDTH = 4
ANGLE_LOOKUP = [
    (0.5, -0.5, math.pi),
    (0.5, 0.5, math.pi / 2),
    (-0.5, 0.5, 0),
    (-0.5, -0.5, math.pi / 2 * 3),
]


class Scene(PlanarSpace):
    def propagate(self: Scene, index: tuple[int, int]) -> bool:  # type: ignore[override]
        x, y = index
        state = self.get((x, y)).state
        return (
            (
                x == 0
                or (
                    (state not in (0, 1) or (self.remove((x - 1, y), [0, 1])))
                    and (state not in (2, 3) or (self.remove((x - 1, y), [2, 3])))
                )
            )
            and (
                x == GRID_SIZE - 1
                or (
                    (state not in (0, 1) or (self.remove((x + 1, y), [0, 1])))
                    and (state not in (2, 3) or (self.remove((x + 1, y), [2, 3])))
                )
            )
            and (
                y == 0
                or (
                    (state not in (0, 3) or (self.remove((x, y - 1), [0, 3])))
                    and (state not in (1, 2) or (self.remove((x, y - 1), [1, 2])))
                )
            )
            and (
                y == GRID_SIZE - 1
                or (
                    (state not in (0, 3) or (self.remove((x, y + 1), [0, 3])))
                    and (state not in (1, 2) or (self.remove((x, y + 1), [1, 2])))
                )
            )
        )

    def is_valid(self: Scene) -> bool:
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if not self.get((x, y)).is_solved:
                    return False
                state = self.get((x, y)).state
                if x < GRID_SIZE - 1:
                    right = self.get((x + 1, y)).state
                    if (state in (0, 1) and right in (0, 1)) or (
                        state in (2, 3) and right in (2, 3)
                    ):
                        return False
                if y < GRID_SIZE - 1:
                    down = self.get((x, y + 1)).state
                    if (state in (0, 3) and down in (0, 3)) or (
                        state in (1, 2) and down in (1, 2)
                    ):
                        return False
        return True

    def draw(
        self: Scene,
        surface: pygame.Surface,
    ) -> None:
        pygame.draw.rect(
            surface,
            FILL_COLOR,
            (0, 0, DRAW_SIZE[0], DRAW_SIZE[1]),
        )
        step = ((DRAW_SIZE[0] - 1) / GRID_SIZE, (DRAW_SIZE[1] - 1) / GRID_SIZE)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                postion = self.get((x, y))
                color = (
                    LINE_COLOR
                    if postion.is_solved
                    else EDGE_COLOR
                    if (x, y) in self.edge
                    else STATE_COLOR
                )
                for state in postion.states:
                    xx, yy, angle = ANGLE_LOOKUP[state]
                    pygame.draw.arc(
                        surface,
                        color,
                        (
                            (x + xx) * step[0] - LINE_WIDTH / 2,
                            (y + yy) * step[1] - LINE_WIDTH / 2,
                            step[0] + LINE_WIDTH,
                            step[1] + LINE_WIDTH,
                        ),
                        angle,
                        angle + math.pi / 2,
                        LINE_WIDTH,
                    )

    def __str__(self: Scene) -> str:
        return "\n".join(
            "".join(str(i) if i is not None else " " for i in row)
            for row in self.matrix
        )


def draw_wait(scene: Scene, window: pygame.Surface, surface: pygame.Surface) -> None:
    scene.draw(surface)
    flush_surface(window, surface)
    await_key(seconds=FRAME_DELAY)


def run() -> None:
    random.seed(0)
    window, surface = setup_surface("Solve Loop", DRAW_SIZE, DRAW_SCALE)
    scene = Scene(count=STATE_COUNT, size=(GRID_SIZE, GRID_SIZE))
    solved = solve(
        scene,
        lambda s: draw_wait(s, window, surface),  # type: ignore[arg-type]
    )
    valid = scene.is_valid()
    pygame.display.set_caption(
        ("SOLVED" if valid and solved else "UNSOLVED" if valid else "INVALID")
        + " (ESC to exit)",
    )
    draw_wait(scene, window, surface)
    await_key()
