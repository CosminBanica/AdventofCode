import re
import time
from day17.cave import *

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
INPUT = SMALL_IN if DEBUG else BIG_IN
JET = ""
CAVE = Cave()
CAVE_DEPTH = 5000
CAVE_WIDTH = 7


def read_input():
    global JET, CAVE

    with open(INPUT) as f:
        lines = f.readlines()
        JET += lines[0].strip()

    print(JET)

    CAVE = Cave(CAVE_DEPTH, CAVE_WIDTH, JET)


def solve_task1():
    for i in range(2022):
        rock = Rock(CAVE.get_spawn_y(), i % 5)
        # print(rock)
        # print("falling from ", CAVE.spawn_height)

        while True:
            CAVE.push_rock(rock)
            if not CAVE.can_lower_rock(rock):
                CAVE.place_rock(rock)
                break
            CAVE.lower_rock(rock)

    return CAVE.spawn_height - 4


if __name__ == '__main__':
    read_input()

    print("Starting task 1")
    start = time.time()
    result = solve_task1()
    print('Task 1 result:' + str(result))
    end = time.time()
    print("Exec time" + str(end - start))

    # print("\nStarting task 2")
    # start = time.time()
    # result = solve_task2()
    # print('Task 2 result:' + str(result))
    # end = time.time()
    # print("Exec time" + str(end - start))