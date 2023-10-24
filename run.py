"""Run solvers."""

import sys
from pathlib import Path

import src.automata
import src.loops
import src.sudoku
import src.sudoku_mini

SECOND = 2

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "sudoku":
            src.sudoku.run(
                Path(sys.argv[SECOND]) if len(sys.argv) > SECOND else None,
            )
        if sys.argv[1] == "sudoku_mini":
            src.sudoku_mini.run(Path(sys.argv[SECOND]))
        elif sys.argv[1] == "loops":
            src.loops.run()
        elif sys.argv[1] == "automata":
            src.automata.run()
        else:
            sys.stderr.write(f"Unknown script: {sys.argv[1]}\n")
    else:
        sys.stderr.write("Usage: python -m src.run <script> [args]\n")
