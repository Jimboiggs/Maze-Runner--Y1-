from typing import Optional

from maze import create_maze
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
