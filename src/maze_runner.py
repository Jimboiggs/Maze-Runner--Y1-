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

            # Load full file into raw_lines
            f.seek(0)
            raw_lines = [line.rstrip("\n") for line in f]

            entrance_row = None
            for y, row in enumerate(raw_lines):
                if "." in row and not row.startswith("#.") and not row.endswith(".#"):
                    entrance_row = y
                    break

            exit_row = None
            for y in range(len(raw_lines) - 1, -1, -1):
                row = raw_lines[y]
                if "." in row and not row.startswith("#.") and not row.endswith(".#"):
                    exit_row = y
                    break

            if exit_row is None:
                raise ValueError("No exit found in maze")

            ascii_exit_x = raw_lines[exit_row].index(".")
            ascii_exit_y = exit_row

            goal_x = ascii_exit_x
            goal_y = ascii_exit_y

            maze["goal"] = (goal_x, goal_y)

            # Check outer walls
            for ch in raw_lines[0]:
                if ch != "#":
                    raise ValueError("Top wall must be fully enclosed")

            for ch in raw_lines[-1]:
                if ch != "#":
                    raise ValueError("Bottom wall must be fully enclosed")

            expected_width = len(raw_lines[0])

            for idx, row in enumerate(raw_lines):
                if len(row) != expected_width:
                    raise ValueError(f"Row {idx} is not rectangular")

                row = row.rstrip("\n")

                if row[0] != "#":
                    raise ValueError(f"Left wall broken at row {idx}")

                if row[-1] != "#":
                    raise ValueError(f"Right wall broken at row {idx}")

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
    starting = starting or (0, 1)
    goal = maze.get("goal", goal)

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
