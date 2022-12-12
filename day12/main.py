from queue import Queue
import string
import time

MAP = []
VISITED = {}
QUEUE = Queue(0)
START = (0, 0)
END = (0, 0)
STARTING_POSITIONS = []


def read_input(file):
    global MAP, START, END
    i = 0
    j = 0

    for x in file:
        if not x.isspace():
            line = []

            for c in x[:-1]:
                if c == 'S':
                    line.append(0)
                    START = (i, j)
                    STARTING_POSITIONS.append(START)
                elif c == 'E':
                    line.append(25)
                    END = (i, j)
                else:
                    d = string.ascii_lowercase.index(c)
                    if d == 0:
                        STARTING_POSITIONS.append((i, j))
                    line.append(d)
                j += 1
            j = 0
            MAP.append(line)
        i += 1


def get_possible_moves(state):
    moves = []
    i = state[0][0]
    j = state[0][1]

    if i > 0:
        moves.append((i - 1, j))

    if i < (len(MAP) - 1):
        moves.append((i + 1, j))

    if j > 0:
        moves.append((i, j - 1))

    if j < (len(MAP[0]) - 1):
        moves.append((i, j + 1))

    ret = []
    for move in moves:
        if (move not in VISITED) and ((MAP[move[0]][move[1]] - MAP[i][j]) <= 1):
            ret.append(move)

    return ret


def find_best_solution(task):
    global QUEUE, VISITED
    ret = -1

    while not QUEUE.empty():
        curr_state = QUEUE.get()

        if curr_state[0] == END:
            ret = curr_state[1]
            break

        moves = get_possible_moves(curr_state)
        curr_depth = curr_state[1]

        for move in moves:
            VISITED[move] = 1
            QUEUE.put((move, curr_depth + 1))

    return ret


def solve_task1():
    global QUEUE, VISITED

    QUEUE.put((START, 0))
    VISITED[START] = 1
    ret = find_best_solution(1)

    QUEUE = Queue(0)
    VISITED = {}

    return ret


def solve_task2():
    global QUEUE, VISITED
    ret = 500000

    while STARTING_POSITIONS:
        first_pos = STARTING_POSITIONS.pop(0)

        QUEUE.put((first_pos, 0))
        VISITED[first_pos] = 1
        depth = find_best_solution(2)

        if depth != -1:
            if depth < ret:
                ret = depth

        QUEUE = Queue(0)
        VISITED = {}

    return ret


if __name__ == '__main__':
    f = open('input.txt', "r")
    read_input(f)

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
