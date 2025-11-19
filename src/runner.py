import maze
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
        runner["y"] += 1
    elif runner["orientation"] == "S":
        runner["y"] -= 1
    elif runner["orientation"] == "E":
        runner["x"] += 1
    elif runner["orientation"] == "W":
        runner["x"] -= 1

    return runner


def sense_walls(runner, maze) -> tuple[bool, bool, bool]:
    front = False
    left = False
    right = False

    if runner["orientation"] == "N":
        if (get_x(runner), get_y(runner) + 1) in maze["horizontal walls"]:
            front = True
        if (get_x(runner), get_y(runner)) in maze["vertical walls"]:
            left = True
        if (get_x(runner) + 1, get_y(runner)) in maze["vertical walls"]:
            right = True
    elif runner["orientation"] == "S":
        if (get_x(runner), get_y(runner)) in maze["horizontal walls"]:
            front = True
        if (get_x(runner), get_y(runner)) in maze["vertical walls"]:
            right = True
        if (get_x(runner) + 1, get_y(runner)) in maze["vertical walls"]:
            left = True
    elif runner["orientation"] == "E":
        if (get_x(runner), get_y(runner)) in maze["horizontal walls"]:
            right = True
        if (get_x(runner), get_y(runner) + 1) in maze["horizontal walls"]:
            left = True
        if (get_x(runner) + 1, get_y(runner)) in maze["vertical walls"]:
            front = True
    elif runner["orientation"] == "W":
        if (get_x(runner), get_y(runner)) in maze["horizontal walls"]:
            left = True
        if (get_x(runner), get_y(runner) + 1) in maze["horizontal walls"]:
            right = True
        if (get_x(runner), get_y(runner)) in maze["vertical walls"]:
            front = True
    return left, front, right


def go_straight(runner: dict, maze: dict) -> dict:
    if sense_walls(runner, maze)[1]:
        raise ValueError("Cannot go straight, there is a wall")
    else:
        forward(runner)
    return runner


def move(runner: dict, maze: dict):
    if not sense_walls(runner, maze)[0]:
        turn(runner, "Left")
        go_straight(runner, maze)
        action = "LF"
    elif not sense_walls(runner, maze)[1]:
        go_straight(runner, maze)
        action = "F"
    elif not sense_walls(runner, maze)[2]:
        turn(runner, "Right")
        go_straight(runner, maze)
        action = "RF"
    else:
        turn(runner, "Left")
        turn(runner, "Left")
        go_straight(runner, maze)
        action = "BF"

    return runner, action


def explore(
    runner, maze, goal: Optional[tuple[int, int]]
) -> list[tuple[int, int, str]]:
    solved = False
    player_action = ""
    returnList = []

    if goal is None:
        goal = (maze["width"] - 1, maze["height"] - 1)

    while not solved:
        runner, player_action = move(runner, maze)
        returnList.append((runner["x"], runner["y"], player_action))
        if runner["x"] == goal[0] and runner["y"] == goal[1]:
            solved = True
    return returnList
