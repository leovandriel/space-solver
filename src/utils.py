# ruff: noqa: D100 D101 D102 D103 D105 D107

from __future__ import annotations

import sys
import time

from src.pygame import pygame

EXIT_KEY = pygame.K_ESCAPE
NEXT_KEY = pygame.K_SPACE


def setup_surface(
    title: str,
    size: tuple[int, int],
    scale: float = 1,
) -> tuple[pygame.Surface, pygame.Surface]:
    pygame.init()
    pygame.display.set_caption(title)
    window = pygame.display.set_mode((size[0] / scale, size[1] / scale))
    surface = pygame.Surface(size)
    return (window, surface)


def flush_surface(window: pygame.Surface, surface: pygame.Surface) -> None:
    window_size = window.get_rect().size
    if surface.get_rect().size[0] > window_size[0]:
        window.blit(pygame.transform.smoothscale(surface, window_size), (0, 0))
    else:
        window.blit(pygame.transform.scale(surface, window_size), (0, 0))
    pygame.display.update()


def await_key(seconds: float | None = None) -> None:
    t = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == EXIT_KEY
            ):
                pygame.quit()
                sys.exit()
                return
            if event.type == pygame.KEYDOWN and event.key == NEXT_KEY:
                return
        if seconds is not None and time.time() - t > seconds:
            return
