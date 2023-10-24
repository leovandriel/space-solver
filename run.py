"""Run solvers."""

import sys
from pathlib import Path

import src.loops
import src.sudoku
import src.sudoku_mini

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "sudoku":
            src.sudoku.run(
                Path(sys.argv[2]) if len(sys.argv) > 2 else None,  # noqa: PLR2004
            )
        if sys.argv[1] == "sudoku_mini":
            src.sudoku_mini.run(Path(sys.argv[2]))
        elif sys.argv[1] == "loops":
            src.loops.run()
        else:
            sys.stderr.write(f"Unknown script: {sys.argv[1]}\n")
    else:
        sys.stderr.write("Usage: python -m src.run <script> [args]\n")
