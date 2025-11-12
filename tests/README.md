# 2526 - COMP1312 - Coursework Tests
This repository contains some tests for the ECS Maze Runner coursework (AY2025-26).

## Getting Started
- You are recommended to clone this repository using SSH
```
git clone git@git.soton.ac.uk:comp1312/2526-Coursework-Tests.git
```
or using HTTPS
```
https://git.soton.ac.uk/comp1312/2526-Coursework-Tests.git
```
The advantage of using git is that you will get the updated versions of the test
suit when they are released.

- Alternatively, you can download the various files directly from this repository.

- The test suit is organised in several test files. You are expected to extend
the test suit with more tests of your own.
  
  - `test_runner.py`: Some unit tests for testing the functionality of 
    `runner.py` including creating a runner, turn, and move the runner forward.
  - `test_maze.py`: Some initial unit tests for testing the functionality of
    `maze.py` including creating a maze, add horizontal and vertical walls.
  - `test_maze_runner.py`: Some initial unit tests for testing the maze runner
    (in `runner.py` for Part 3) including sensing information, safe going
    forward, move and explore the maze.
  - `test_shortest_path.py`: Some initial unit tests for testing the
    `shortest_path` function (in `maze_runner.py` for Part 4).
  - `test_maze_reader.py`: Some initial unit tests for testing the
    `maze_reader()` function (in `maze_runner.py` for Part 5).
  - `utils.py`: A `render()` function to display a maze.

- Folder `mazes` contains some mazes of different sizes for manual testing.
  - Contributions from Josh Wilcox (COMP1312 - AY2024-25) and
  Tom Purnell (COMP1312 - AY2024-25)

## Authors and Acknowledgement
The current maintainer for this repository is
[H.Packer](mailto:hsp2m10 at soton dot ac dot uk).

The code is derived from code developed for AY2024-25 by
[T.S.Hoang](mailto:T dot S dot Hoang at soton dot ac dot uk).

## License
The code in this repository is licenced under the MIT License and can be seen in
the `LICENSE.md` file.
