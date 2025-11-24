from typing import Optional

from runner import explore
from runner import create_runner
from maze import create_maze


def shortest_path(
    maze, starting: Optional[tuple[int, int]], goal: Optional[tuple[int, int]]
) -> list[tuple[int, int, str]]:
    if starting is None:
        starting = (0, 0)
    if goal is None:
        goal = (maze["width"] - 1, maze["height"] - 1)

    runner = create_runner(starting[0], starting[1])
    path = explore(runner, maze, goal)
    print(path)

    previous = []
    for i in range(len(path)):
        if path[i] not in previous:
            previous.append(path[i])
        else:
            j = previous.index(path[i])
            for k in range(j - i):
                del path[j - k]

    return path


def maze_reader(maze_file: str) -> dict:
    try:
        with open(maze_file) as f:
            lines = 0
            width = 0

            # Checks
            allowed = {"#", ".", "\n"}
            first = f.readline().rstrip()
            for line in f:
                for ch in line:
                    if ch not in allowed:
                        raise ValueError("File must contain only '.' '#'")
                lines += 1
                width = len(line)
                last = line
            height = lines // 2

            # Initialise maze
            maze = create_maze(width, height)

            # Check outer walls
            last = last.rstrip()
            for j in range(len(last)):
                if first[j] != "#" or last[j] != "#":
                    raise ValueError("Maze must be enclosed with walls")
                elif len(line) != width:
                    raise ValueError("Maze must be rectangular")
            f.seek(0)
            for k in f:
                if k[0] != "#" or k[-1] != "#":
                    raise ValueError("Maze must be enclosed with walls")

            # Actual wall logic
            f.seek(0)
            y = 0
            for line in f:
                line = line.rstrip("\n")
                x = 0
                while x < len(line):
                    ch = line[x]
                    if ch == "#":
                        if y % 2 == 0:
                            maze["horizontal walls"].append((x, y))
                        elif x % 2 == 0:
                            maze["vertical walls"].append((x, y))
                    x += 1
                y += 1

            return maze

    except Exception as e:
        raise IOError("Error reading maze file")
