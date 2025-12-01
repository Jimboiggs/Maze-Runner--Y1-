from typing import Optional
import argparse

inputFile = None
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
    global inputFile
    inputFile = maze_file
    try:
        with open(maze_file) as f:
            lines = 0
            width = 0

            # Checks
            allowed = {"#", ".", "\n"}
            first = f.readline().rstrip()

            while len(first) < 3:
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

            exit_x = None
            bottom = last.rstrip("\n")

            for x, ch in enumerate(bottom):
                if ch == ".":  # an opening in the wall
                    exit_x = x
                    break

            if exit_x is None:
                raise ValueError("No exit found in maze")

            goal_x = exit_x // 2
            goal_y = (lines - 1) // 2  # bottom cell row
            maze["goal"] = (goal_x, goal_y)

            # Check outer walls
            # last = last.rstrip()
            # for j in range(len(last)):
            # if first[j] != "#" or last[j] != "#":
            # raise ValueError("Maze must be enclosed with walls")
            # elif len(line) != width:
            # raise ValueError("Maze must be rectangular")
            # f.seek(0)
            # for k in f:
            # if k[0] != "#" or k[-1] != "#":
            # raise ValueError("Maze must be enclosed with walls")

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ECS Maze Runner")
    parser.add_argument("maze", help="The name of the maze file, e.g., maze1.mz")
    parser.add_argument("--starting", help="The starting position, e.g., 2, 1")
    parser.add_argument("--goal", help="The goal position, e.g., 4, 5")
    args = parser.parse_args()

    # Inline parsing of positions
    if args.starting:
        try:
            starting = tuple(map(int, args.starting.replace(" ", "").split(",")))
        except Exception:
            raise ValueError(
                f"Invalid starting position format: {args.starting}. Expected 'x, y'."
            )
    else:
        starting = None

    if args.goal:
        try:
            goal = tuple(map(int, args.goal.replace(" ", "").split(",")))
        except Exception:
            raise ValueError(
                f"Invalid goal position format: {args.goal}. Expected 'x, y'."
            )
    else:
        goal = None

    if starting is None:
        runner = create_runner(0, 0)
    else:
        runner = create_runner(starting[0], starting[1])

    maze = maze_reader(args.maze)

    exploration = explore(runner, maze, goal)
    shortest = shortest_path(maze, starting, goal)

    # .txt file support
    with open("statistics.txt", "w") as statsFile:
        statsFile.write("Input file: " + str(inputFile) + "\n")
        score = len(exploration) / (4 + len(shortest))
        statsFile.write("Score: " + str(score) + "\n")
        statsFile.write("Number of steps: " + str(len(exploration)) + "\n")
        statsFile.write("Shortest path: " + str(shortest) + "\n")
        statsFile.write("Length of shortest path: " + str(len(shortest)) + "\n")

    print(f"Maze file: {args.maze}")
    print(f"Starting position: {starting}")
    print(f"Goal position: {goal}")
