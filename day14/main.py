import time

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
MAP = []
MAP_TASK2 = []
BUFFER = 485
WIDTH = 1000
HEIGHT = 185  # 185 or 10
START = (500 - BUFFER, 0)


def read_input():
    global MAP

    MAP.append([i + BUFFER for i in range(WIDTH)])
    MAP_TASK2.append([i + BUFFER for i in range(WIDTH)])

    for i in range(1, HEIGHT):
        MAP.append([])
        MAP_TASK2.append([])
        for j in range(WIDTH):
            MAP[i].append('.')
            MAP_TASK2[i].append('.')

    with open(BIG_IN) as f:
        lines = f.readlines()

    for line in lines:
        if not line.isspace():
            points = line[:-1].split(" -> ")

            for i in range(len(points) - 1):
                x1, y1 = points[i].split(",")
                x2, y2 = points[(i + 1)].split(",")

                for x in range(min(int(x1), int(x2)), max(int(x1), int(x2)) + 1):
                    for y in range(min(int(y1), int(y2)), max(int(y1), int(y2)) + 1):
                        MAP[y][x - BUFFER] = '#'
                        MAP_TASK2[y][x - BUFFER] = '#'

    for j in range(WIDTH):
        MAP_TASK2[len(MAP_TASK2) - 1][j] = '#'


def print_map(map_nr):
    map_to_print = []
    if map_nr == 1:
        map_to_print = MAP
    else:
        map_to_print = MAP_TASK2

    for j in range(WIDTH):
        print(str(map_to_print[0][j]) + " ", end='')
    print()

    for i in range(1, HEIGHT):
        for j in range(WIDTH):
            print(str(map_to_print[i][j]) + "   ", end="")
        print()


def solve_task1():
    global MAP
    ret = 0

    sand = START

    while True:
        if sand[1] == HEIGHT - 1:
            break

        if MAP[sand[1] + 1][sand[0]] == '.':
            sand = (sand[0], sand[1] + 1)
        elif MAP[sand[1] + 1][sand[0]] == '#' and MAP[sand[1] + 1][sand[0] - 1] == '.':  # left
            sand = (sand[0] - 1, sand[1] + 1)
        elif MAP[sand[1] + 1][sand[0]] == '#' and MAP[sand[1] + 1][sand[0] + 1] == '.':  # right
            sand = (sand[0] + 1, sand[1] + 1)
        elif MAP[sand[1] + 1][sand[0]] == '#' and MAP[sand[1] + 1][sand[0] - 1] == '#' and MAP[sand[1] + 1][sand[0] + 1] == '#':
            MAP[sand[1]][sand[0]] = '#'
            ret += 1
            sand = START

    return ret


def solve_task2():
    global MAP_TASK2
    ret = 0
    sand = START

    while True:
        # print("sand is at: " + str(sand))
        if MAP_TASK2[sand[1] + 1][sand[0]] == '.':
            sand = (sand[0], sand[1] + 1)
        elif MAP_TASK2[sand[1] + 1][sand[0]] == '#' and MAP_TASK2[sand[1] + 1][sand[0] - 1] == '.':  # left
            sand = (sand[0] - 1, sand[1] + 1)
        elif MAP_TASK2[sand[1] + 1][sand[0]] == '#' and MAP_TASK2[sand[1] + 1][sand[0] + 1] == '.':  # right
            sand = (sand[0] + 1, sand[1] + 1)
        elif MAP_TASK2[sand[1] + 1][sand[0]] == '#' and MAP_TASK2[sand[1] + 1][sand[0] - 1] == '#' and MAP_TASK2[sand[1] + 1][sand[0] + 1] == '#':
            MAP_TASK2[sand[1]][sand[0]] = '#'
            ret += 1

            if sand == START:
                break

            sand = START

    return ret


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