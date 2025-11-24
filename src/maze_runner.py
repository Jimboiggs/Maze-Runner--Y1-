from typing import Optional

from runner import explore
from runner import create_runner


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
            height = 0
            width = 0
            first = f.readline().rstrip()
            for line in f:
                height += 1
                width = len(line)
                last = line

            # Check outer walls
            last = last.rstrip()
            for j in range(len(last)):
                if first[j] != "#" or last[j] != "#":
                    raise ValueError("Maze must be enclosed with walls")
            for k in f:
                if k[0] != "#" or k[-1] != "#":
                    raise ValueError("Maze must be enclosed with walls")

            maze = {
                "height": height,
                "width": width,
            }
            return maze

    except:
        raise IOError("Error reading maze file")
