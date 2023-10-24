"""Wrap pygame to hide the pygame support prompt."""

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame as pygame  # noqa: PLC0414 E402
