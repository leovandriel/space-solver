<img src="logo.jpg" width="25%" height="25%" align="right" alt="logo">

# Spatial Solver

Generic constraint solver based on state collapse.

<img src="sudoku.png" width="50%" height="50%" alt="Solve Sudoku">

[Video](https://www.youtube.com/watch?v=zSskltnm2YI)

<img src="loops.png" width="50%" height="50%" alt="Solve Loops">

[Video](https://www.youtube.com/watch?v=aOl-y7EOkps)

<img src="automata.png" width="50%" height="50%" alt="Solve Rule 30">

[Video](https://www.youtube.com/watch?v=aVtnLfdKUps)

## Usage

Fill plane with loops:

    python -m run loops

Solve sudoku (CLI, no animation):

    python -m run sudoku_mini data/sudoku/expert.txt

Solve sudoku (animated):

    python -m run sudoku data/sudoku/expert.txt

Attempt to fill plane with Wolfram rule 30:

    python -m run automata

## License

MIT
