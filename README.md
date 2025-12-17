This project solves mazes with the left-hug algorithm, producing a path. The path is then modified to produce a ‘shortest path’ by not visiting dead ends (this is not always the actual shortest path, but the most optimal found by the algorithm). The log of the maze solver is stored in a .csv file and information about the shortest path and number of steps is written to a .txt file. Mazes can be read from a .mz file. The contents of the file are verified to contain a valid maze, and this data is then used to construct a maze for the algorithm to solve. I have tested the algorithm with a large range of maze sizes. You can also input the start and goal coordinates manually (see bellow), or use the default start position and detected goal position. Throughout the development of this project, I used Github for source control, created different modules (maze.py, maze_runner.py and runner.py) and used a range of data types.

The maze solver takes arguments from the command line using argparse. You can run maze_runner.py with the following parameters:
* Maze file (.mz)
* Starting position (optional)
* Goal position (optional)
For example:
python maze_runner.py ../tests/mazes/doom_maze.mz --starting 1,1 --goal 10,5
python maze_runner.py ../tests/mazes/tiny_maze1.mz

The python files can be found in the ‘src’ folder and the folder of test maze files can be found within the ‘test’ folder.

Maze example:


<img width="265" height="485" alt="Maze Example" src="https://github.com/user-attachments/assets/f2dbbf94-ee77-46c0-b0da-f7b52ca6529e" />
