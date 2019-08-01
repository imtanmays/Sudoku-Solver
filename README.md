# SudokuSolver
Using CSP techniques like backtracking, forward checking, and heuristic selection to solve sudoku puzzles

### The relevant files in this repo include:
- *SudokuSolver.py* - Python code that implements three versions/algorithms (A,B,C) to solve sudoku puzzle
- *sudoku_problems* - folder that contains unsolved puzzles to test SudokuSolver.py

### Running SudokuSolver.py:
- Ensure you have Python 3.7 installed on machine
- Use the prompts below to determine testing file and algorithm used to solve puzzle

###### Example: Here are the sequence of inputs you should provide if you would like to run backtracking (version A) on file sudoku_problems/47/10.sd
```
python3 SudokuSolver.py
Enter no. of initial values (1-71): 47
Enter test file (1-10): 10
Which version/algorithm would you like to use to solve the sudoku puzzle? Enter either <A, B, or C>: A
```
###### Example: Here are the sequence of inputs you should provide if you would like to run backtracking + forward checking (version B) on file sudoku_problems/34/1.sd

```
python3 SudokuSolver.py
Enter no. of initial values (1-71): 34
Enter test file (1-10): 1
Which version/algorithm would you like to use to solve the sudoku puzzle? Enter either <A, B, or C>: B
```
