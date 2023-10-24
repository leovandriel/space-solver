# ruff: noqa: D100 D101 D102 D103 D105 D107

from __future__ import annotations

import random
from typing import cast

from src.position import DiscretePosition
from src.pygame import pygame
from src.solver import solve_space
from src.space import PlanarSpace, SpaceIndex
from src.utils import await_key, flush_surface, setup_surface

FRAME_DELAY = 0.01
STATE_COUNT = 6
GRID_SIZE = (100, 100)
DRAW_SCALE = 0.2
COLOR_0 = (255, 255, 255)
COLOR_1 = (0, 0, 0)
UNSOLVED_COLOR = (128, 128, 128)
EDGE_COLOR = (255, 128, 0)

rule30 = [
    (1, 1, 1, 0),
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (1, 0, 0, 1),
    (0, 1, 1, 1),
    (0, 1, 0, 1),
    (0, 0, 1, 1),
    (0, 0, 0, 0),
]

rule_offset = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (0, 0),
]

UNSET = 2
UNSOLVED = 3
EMPTY_POSITION = DiscretePosition(size=STATE_COUNT)


def in_bounds(index: SpaceIndex) -> bool:
    x, y = cast(tuple[int, int], index)
    return x >= 0 and x <= GRID_SIZE[0] - 1 and y >= 0 and y <= GRID_SIZE[1] - 1


class Scene(PlanarSpace):
    def propagate(self: Scene, index: SpaceIndex) -> bool:
        if self.get(index).state > 1:
            return False
        current = cast(tuple[int, int], index)
        for offset in rule_offset:
            indices = [
                (current[0] + off[0] - offset[0], current[1] + off[1] - offset[1])
                for off in rule_offset
            ]
            positions = [
                self.get(idx) if in_bounds(idx) else EMPTY_POSITION for idx in indices
            ]
            states = [pos.state if pos.is_solved else None for pos in positions]
            solves = [UNSET] * 4
            found = False
            for rule in rule30:
                if all(
                    state is None or state == part for state, part in zip(states, rule)
                ):
                    found = True
                    solves = [
                        solve
                        if state is not None
                        else part
                        if solve in (UNSET, part)
                        else UNSOLVED
                        for state, part, solve in zip(states, rule, solves)
                    ]
            if not found:
                return False
            for i, solve, idx in zip(range(4), solves, indices):
                if in_bounds(idx):
                    if solve in (0, 1) and not self.solve(idx, solve):
                        return False
                    if solve == UNSOLVED and not self.remove(idx, [2 + i]):
                        return False
        return True

    def draw(
        self: Scene,
        surface: pygame.Surface,
    ) -> None:
        for y in range(GRID_SIZE[1]):
            for x in range(GRID_SIZE[0]):
                position = self.get((x, y))
                color = (
                    EDGE_COLOR
                    if (x, y) in self.edge
                    else UNSOLVED_COLOR
                    if not position.is_solved
                    else COLOR_0
                    if position.state == 0
                    else COLOR_1
                )
                surface.set_at((x, y), color)


def draw_wait(scene: Scene, window: pygame.Surface, surface: pygame.Surface) -> None:
    scene.draw(surface)
    flush_surface(window, surface)
    await_key(seconds=FRAME_DELAY)


def run() -> None:
    random.seed(0)
    window, surface = setup_surface("Solve Rule 30", GRID_SIZE, DRAW_SCALE)
    scene = Scene(count=STATE_COUNT, size=GRID_SIZE)
    scene.edge.add((GRID_SIZE[0] // 2, GRID_SIZE[1] // 2))
    solved = solve_space(
        scene,
        lambda s: draw_wait(cast(Scene, s), window, surface),
    )
    pygame.display.set_caption(
        ("SOLVED" if solved else "UNSOLVED") + " (ESC to exit)",
    )
    draw_wait(scene, window, surface)
    await_key()
