import csv
from typing import Optional


def create_runner(x: int = 0, y: int = 0, orientation: str = "N"):
    runner = {
        "x": x,
        "y": y,
        "orientation": orientation,
    }
    return runner


def get_x(runner: dict):
    return runner["x"]


def get_y(runner: dict):
    return runner["y"]


def get_orientation(runner):
    return runner["orientation"]


def turn(runner: dict, direction: str):
    directions = ["N", "E", "S", "W"]
    i = directions.index(runner["orientation"])

    if direction == "Left":
        i -= 1
    else:
        i += 1

    if i > 3:
        i -= 4
    elif i < 0:
        i += 4

    runner["orientation"] = directions[i]
    return runner


def forward(runner: dict):
    if runner["orientation"] == "N":
        runner["y"] -= 1
    elif runner["orientation"] == "S":
        runner["y"] += 1
    elif runner["orientation"] == "E":
        runner["x"] += 1
    elif runner["orientation"] == "W":
        runner["x"] -= 1

    return runner


def sense_walls(runner, maze):
    x, y = get_x(runner), get_y(runner)
    direction = runner["orientation"]
    grid = maze["grid"]

    if direction == "N":
        front = (x, y - 1)
        left = (x - 1, y)
        right = (x + 1, y)
    elif direction == "S":
        front = (x, y + 1)
        left = (x + 1, y)
        right = (x - 1, y)
    elif direction == "E":
        front = (x + 1, y)
        left = (x, y - 1)
        right = (x, y + 1)
    elif direction == "W":
        front = (x - 1, y)
        left = (x, y + 1)
        right = (x, y - 1)

    return (
        is_wall(grid, left),
        is_wall(grid, front),
        is_wall(grid, right),
    )


def is_wall(grid, pos):
    x, y = pos
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[0]):
        return True
    return grid[y][x] == "#"


def go_straight(runner: dict, maze: dict) -> dict:
    if sense_walls(runner, maze)[1]:
        raise ValueError("Cannot go straight, there is a wall")
    else:
        forward(runner)
    return runner


def move(runner, maze, step, log):
    left, front, right = sense_walls(runner, maze)

    # Left-hand rule:
    # 1. If left is open → turn left, then move forward
    if not left:
        turn(runner, "Left")
        player_action = "L"
        step += 1
        log.append((get_x(runner), get_y(runner), player_action))

        forward(runner)
        player_action = "F"
        step += 1
        log.append((get_x(runner), get_y(runner), player_action))

        return runner, player_action, step, log

    # 2. If front is open → move forward
    if not front:
        forward(runner)
        player_action = "F"
        step += 1
        log.append((get_x(runner), get_y(runner), player_action))

        return runner, player_action, step, log

    # 3. If right is open → turn right, then move forward
    if not right:
        turn(runner, "Right")
        player_action = "R"
        step += 1
        log.append((get_x(runner), get_y(runner), player_action))

        forward(runner)
        player_action = "F"
        step += 1
        log.append((get_x(runner), get_y(runner), player_action))

        return runner, player_action, step, log

    # 4. Dead end → turn around (two left turns), then move forward
    turn(runner, "Left")
    turn(runner, "Left")
    player_action = "B"  # Backtrack turn
    step += 1
    log.append((get_x(runner), get_y(runner), player_action))

    forward(runner)
    player_action = "F"
    step += 1
    log.append((get_x(runner), get_y(runner), player_action))

    return runner, player_action, step, log


def explore(
    runner, maze, goal: Optional[tuple[int, int]]
) -> list[tuple[int, int, str]]:
    solved = False
    player_action = ""
    returnList = []

    if goal is None:
        goal = maze.get("goal", (maze["width"] - 1, maze["height"] - 1))

    step = 0
    log = []
    while not solved:
        step += 1
        runner, player_action, step, log = move(runner, maze, step, log)
        returnList.append((runner["x"], runner["y"], player_action))
        if runner["x"] == goal[0] and runner["y"] == goal[1]:
            solved = True

    # log to .csv file
    with open("exploration.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(log)

    return returnList
