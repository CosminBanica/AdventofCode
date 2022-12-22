import copy

from solver_template import solver_template

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
INPUT = SMALL_IN if DEBUG else BIG_IN
RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
CUBE_FACE_SIZE = 4 if DEBUG else 50


class Node:
    def __init__(self, cell, position, up=None, down=None, left=None, right=None):
        self.cell = cell
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.position = position
        self.printed = False
        self.orientation = None

    def __repr__(self):
        self.printed = not self.printed
        return f"{self.cell}{self.right if self.right.printed != self.printed else ''}"


def region(cell_x, cell_y):
    rx = cell_x // CUBE_FACE_SIZE
    ry = cell_y // CUBE_FACE_SIZE
    if (rx, ry) == (0, 1):
        return 5
    if (rx, ry) == (0, 2):
        return 6
    if (rx, ry) == (1, 1):
        return 4
    if (rx, ry) == (2, 1):
        return 3
    if (rx, ry) == (2, 0):
        return 2
    if (rx, ry) == (3, 0):
        return 1


def get_new_cube_position(position, direction):
    i, j = position
    if direction == RIGHT:
        if region(i, j) == 6:
            return (-i + 149, 99), LEFT
        if region(i, j) == 4:
            return (49, i + 50), UP
        if region(i, j) == 3:
            return (-i + 149, 149), LEFT
        if region(i, j) == 1:
            return (149, i - 100), UP
    elif direction == DOWN:
        if region(i, j) == 6:
            return (j - 50, 99), LEFT
        if region(i, j) == 3:
            return (j + 100, 49), LEFT
        if region(i, j) == 1:
            return (0, j + 100), DOWN
    elif direction == LEFT:
        if region(i, j) == 5:
            return (-i + 149, 0), RIGHT
        if region(i, j) == 4:
            return (100, i - 50), DOWN
        if region(i, j) == 2:
            return (-i + 149, 50), RIGHT
        if region(i, j) == 1:
            return (0, i - 100), DOWN
    elif direction == UP:
        if region(i, j) == 6:
            return (199, j - 100), UP
        if region(i, j) == 5:
            return (j + 100, 0), RIGHT
        if region(i, j) == 2:
            return (j + 50, 50), RIGHT


def read_input():
    nodes = {}
    cube_nodes = {}
    path = []
    start_coordinates = None
    row_intervals = {}
    column_intervals = {}

    with open(INPUT) as f:
        lines = f.readlines()

    max_row_length = max([len(line[:-1]) for line in lines[:-2]])
    for i in range(max_row_length):
        column_intervals[i] = [-1, -1]

    for i, line in enumerate(lines[:-2]):
        row_interval = [-1, len(line[:-1]) - 1]
        for j in range(len(line[:-1])):
            if not line[j].isspace():
                nodes[(i, j)] = Node(line[j], (i, j))
                cube_nodes[(i, j)] = Node(line[j], (i, j))
                if column_intervals[j][0] == -1:
                    column_intervals[j][0] = i
                column_intervals[j][1] = i
                if row_interval[0] == -1:
                    row_interval[0] = j

                if line[j] == '.' and not start_coordinates:
                    start_coordinates = (i, j)

        row_intervals[i] = row_interval

    for position in nodes:
        i, j = position
        if (i - 1, j) in nodes:
            nodes[position].up = nodes[(i - 1, j)]
            cube_nodes[position].up = cube_nodes[(i - 1, j)]
        else:
            nodes[position].up = nodes[(column_intervals[j][1], j)]
            new_cube_position, new_orientation = get_new_cube_position(position, UP)
            cube_nodes[position].up = cube_nodes[new_cube_position]
            cube_nodes[position].up.orientation = new_orientation
        if (i + 1, j) in nodes:
            nodes[position].down = nodes[(i + 1, j)]
            cube_nodes[position].down = cube_nodes[(i + 1, j)]
        else:
            nodes[position].down = nodes[(column_intervals[j][0], j)]
            new_cube_position, new_orientation = get_new_cube_position(position, DOWN)
            cube_nodes[position].down = cube_nodes[new_cube_position]
            cube_nodes[position].down.orientation = new_orientation
        if (i, j - 1) in nodes:
            nodes[position].left = nodes[(i, j - 1)]
            cube_nodes[position].left = cube_nodes[(i, j - 1)]
        else:
            nodes[position].left = nodes[(i, row_intervals[i][1])]
            new_cube_position, new_orientation = get_new_cube_position(position, LEFT)
            cube_nodes[position].left = cube_nodes[new_cube_position]
            cube_nodes[position].left.orientation = new_orientation
        if (i, j + 1) in nodes:
            nodes[position].right = nodes[(i, j + 1)]
            cube_nodes[position].right = cube_nodes[(i, j + 1)]
        else:
            nodes[position].right = nodes[(i, row_intervals[i][0])]
            new_cube_position, new_orientation = get_new_cube_position(position, RIGHT)
            cube_nodes[position].right = cube_nodes[new_cube_position]
            cube_nodes[position].right.orientation = new_orientation

    i = 0
    while i < len(lines[-1]):
        command = ""

        if lines[-1][i].isdigit():
            while lines[-1][i].isdigit():
                command += lines[-1][i]
                i += 1
                if i >= len(lines[-1]):
                    break

            command = int(command)
        else:
            command = lines[-1][i]
            i += 1

        path.append(command)

    return nodes, cube_nodes, path, nodes[start_coordinates], cube_nodes[start_coordinates]


def solve_task1(puzzle_data):
    nodes, path, current_node = puzzle_data
    facing_direction = RIGHT

    for command in path:
        if command == 'L':
            facing_direction = (facing_direction - 1) % 4
        elif command == 'R':
            facing_direction = (facing_direction + 1) % 4
        else:
            for _ in range(command):
                if facing_direction == RIGHT:
                    if current_node.right.cell != '#':
                        current_node = current_node.right
                elif facing_direction == DOWN:
                    if current_node.down.cell != '#':
                        current_node = current_node.down
                elif facing_direction == LEFT:
                    if current_node.left.cell != '#':
                        current_node = current_node.left
                else:
                    if current_node.up.cell != '#':
                        current_node = current_node.up

    res = [current_node.position[0] + 1, current_node.position[1] + 1, facing_direction]
    res = 1000 * res[0] + 4 * res[1] + res[2]

    return res


def solve_task2(puzzle_data):
    nodes, path, current_node = puzzle_data
    facing_direction = RIGHT

    for command in path:
        if command == 'L':
            facing_direction = (facing_direction - 1) % 4
        elif command == 'R':
            facing_direction = (facing_direction + 1) % 4
        else:
            for _ in range(command):
                if facing_direction == RIGHT:
                    if current_node.right.cell != '#':
                        if current_node.orientation and current_node.right.orientation:
                            facing_direction = current_node.right.orientation
                        current_node = current_node.right
                elif facing_direction == DOWN:
                    if current_node.down.cell != '#':
                        if current_node.orientation and current_node.down.orientation:
                            facing_direction = current_node.right.orientation
                        current_node = current_node.down
                elif facing_direction == LEFT:
                    if current_node.left.cell != '#':
                        if current_node.orientation and current_node.left.orientation:
                            facing_direction = current_node.right.orientation
                        current_node = current_node.left
                else:
                    if current_node.up.cell != '#':
                        if current_node.orientation and current_node.up.orientation:
                            facing_direction = current_node.right.orientation
                        current_node = current_node.up

    res = [current_node.position[0] + 1, current_node.position[1] + 1, facing_direction]
    res = 1000 * res[0] + 4 * res[1] + res[2]

    return res


if __name__ == '__main__':
    data = read_input()
    task1_data = data[0], data[2], data[3]
    task2_data = data[1], data[2], data[4]
    solver_template(solve_task1=solve_task1, solve_task2=solve_task2, task1_args=task1_data, task2_args=task2_data)
