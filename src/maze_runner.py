from typing import Optional


def shortest_path(
    maze, starting: Optional[tuple[int, int]], goal: Optional[tuple[int, int]]
) -> list[tuple[int, int, str]]:
    if starting is None:
        starting = (0, 0)
    if goal is None:
        goal = (maze["width"] - 1, maze["height"] - 1)
