def create_maze(width: int = 5, height: int = 5):
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
