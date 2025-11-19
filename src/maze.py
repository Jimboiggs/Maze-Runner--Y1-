def create_maze(width: int = 5, height: int = 5) -> dict:
    maze = {
        "width": width,
        "height": height,
        "vertical walls": [],
        "horizontal walls": [],
    }

    for i in range(width):
        maze["horizontal walls"].append((i, 0))
        maze["horizontal walls"].append((i, height))

    for j in range(height):
        maze["vertical walls"].append((0, j))
        maze["vertical walls"].append((width, j))

    return maze


def add_horizontal_wall(maze, x_coordinate, horizontal_line) -> dict:
    maze["horizontal walls"].append((x_coordinate, horizontal_line))
    return maze


def add_vertical_wall(maze, y_coordinate, vertical_line) -> dict:
    maze["vertical walls"].append(vertical_line, y_coordinate)
    return maze


def get_dimensions(maze) -> tuple[int, int]:
    return maze["width"], maze["height"]


def get_walls(
    maze, x_coordinate: int, y_coordinate: int
) -> tuple[bool, bool, bool, bool]:
    north = False
    south = False
    east = False
    west = False

    if (x_coordinate, y_coordinate) in maze["horizontal walls"]:
        south = True
    if (x_coordinate, y_coordinate + 1) in maze["horizontal walls"]:
        north = True
    if (x_coordinate, y_coordinate) in maze["vertical walls"]:
        west = True
    if (x_coordinate + 1, y_coordinate) in maze["vertical walls"]:
        east = True

    return north, east, south, west
