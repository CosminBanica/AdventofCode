import re
import time

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
INPUT = SMALL_IN if DEBUG else BIG_IN
CUBES = []
CUBES_SET = set()
SURFACE_AREA = 0


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def read_input():
    global CUBES, SURFACE_AREA, CUBES_SET

    with open(INPUT) as f:
        lines = f.readlines()

    for line in lines:
        CUBES.append(tuple(map(int, line.split(','))))
        SURFACE_AREA += 6

    CUBES_SET = {tuple([int(x) for x in line.strip().split(',')]) for line in lines}


def solve_task1():
    global SURFACE_AREA

    for i in range(len(CUBES)):
        for j in range(i + 1, len(CUBES)):
            if distance(CUBES[i], CUBES[j]) == 1:
                SURFACE_AREA -= 2

    return SURFACE_AREA


def sides(x, y, z):
    return {(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)}


def solve_task2():
    seen = set()
    todo = [(-1, -1, -1)]

    while todo:
        here = todo.pop()
        todo += [s for s in (sides(*here) - CUBES_SET - seen) if all(-1 <= c <= 25 for c in s)]
        seen |= {here}

    return sum((s in seen) for c in CUBES_SET for s in sides(*c))


if __name__ == '__main__':
    read_input()

    print("Starting task 1")
    start = time.time()
    result = solve_task1()
    print('Task 1 result:' + str(result))
    end = time.time()
    print("Exec time" + str(end - start))

    print("\nStarting task 2")
    start = time.time()
    result = solve_task2()
    print('Task 2 result:' + str(result))
    end = time.time()
    print("Exec time" + str(end - start))
