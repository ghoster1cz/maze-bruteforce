import copy
import sys

NOT_RECT = "Bludiste neni obdelnikove!\n"
BAD_ENTRANCE = "Vstup neni vlevo nahore!\n"
BAD_EXIT = "Vystup neni vpravo dole!\n"
BAD_WIDTH = "Sirka bludiste je mimo rozsah!\n"
BAD_HEIGHT = "Delka bludiste je mimo rozsah!\n"
BAD_CHARACTER = "Bludiste obsahuje nezname znaky!\n"
NOT_FENCED = "Bludiste neni oplocene!\n"

WALL_CHAR = '#'
PATH_CHAR = '.'
IMPORTANT_CHAR = '!'

ENTRANCE_POS = (0, 1)
EXIT_POS = (-1, -2)

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = (DOWN, RIGHT, UP, LEFT)


# //////////////////////////////// UTILS
def print_maze(maze_to_print):
    for row in maze_to_print:
        for col in row:
            print(col, end='')
        print()


def print_error(text):
    print("Error:", text, file=sys.stderr)
    quit(1)


def point_in_paths(point, paths):
    for path in paths:
        if point not in path:
            return False

    return True


def filter_path(paths):
    important_points = []
    for point in paths[0]:
        if point_in_paths(point, paths[1:]):
            important_points.append(point)

    return important_points


# //////////////////////////////// MAZE TESTS
def is_rectangular(maze):
    for row in maze:
        if len(row) != len(maze[0]):
            return False

    return True


def valid_entrance(maze):
    return maze[ENTRANCE_POS[0]][ENTRANCE_POS[1]] == PATH_CHAR


def valid_exit(maze):
    return maze[EXIT_POS[0]][EXIT_POS[1]] == PATH_CHAR


def valid_width(maze):
    return 5 <= len(maze[0]) <= 100


def valid_height(maze):
    return 5 <= len(maze) <= 50


def valid_characters(maze):
    for row in maze:
        for col in row:
            if col not in [WALL_CHAR, PATH_CHAR]:
                return False

    return True


def is_fenced(maze):
    for col in range(len(maze[0])):
        if col != 1:
            if maze[0][col] != WALL_CHAR:
                return False

    for col in range(len(maze[len(maze) - 1])):
        if col != len(maze[0]) - 2:
            if maze[len(maze) - 1][col] != WALL_CHAR:
                return False

    for index in range(len(maze)):
        if maze[index][0] != WALL_CHAR or maze[index][len(maze[0]) - 1] != WALL_CHAR:
            return False

    return True

# //////////////////////////////// MAZE TESTER
def check_maze(maze):
    if not is_rectangular(maze):
        print_error(NOT_RECT)

    if not valid_entrance(maze):
        print_error(BAD_ENTRANCE)

    if not valid_exit(maze):
        print_error(BAD_EXIT)

    if not valid_width(maze):
        print_error(BAD_WIDTH)

    if not valid_height(maze):
        print_error(BAD_HEIGHT)

    if not valid_characters(maze):
        print_error(BAD_CHARACTER)

    if not is_fenced(maze):
        print_error(NOT_FENCED)


# //////////////////////////////// INPUT HELPER
def read_input():
    maze = []
    for line in sys.stdin.readlines():
        maze.append([x for x in line if x != '\n'])

    return maze


# //////////////////////////////// BACKTRACKING

def start_backtrack(input_maze):
    backtrack_maze = copy.deepcopy(input_maze)
    paths = []

    backtrack_recursion(backtrack_maze, ENTRANCE_POS, [], paths)
    return paths


def backtrack_recursion(backtrack_maze, pos, taken_path, paths):
    if backtrack_maze[pos[0]][pos[1]] == WALL_CHAR or pos in taken_path:
        return

    taken_path.append(pos)
    exit_pos = (len(maze) + EXIT_POS[0], len(maze[0]) + EXIT_POS[1])

    if pos == exit_pos:
        paths.append(taken_path.copy())
        taken_path.pop()
        return

    for direction in DIRECTIONS:
        new_pos = tuple(map(lambda coord, orientation: coord + orientation, pos, direction))
        backtrack_recursion(backtrack_maze, new_pos, taken_path, paths)

    taken_path.pop()


if __name__ == "__main__":
    maze = read_input()
    check_maze(maze)

    points = filter_path(start_backtrack(maze))
    for point in points:
        maze[point[0]][point[1]] = IMPORTANT_CHAR
    print_maze(maze)
