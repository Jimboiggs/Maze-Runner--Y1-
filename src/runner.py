


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
