import ast
import functools
import time

PAIRS = []
PACKETS = []
SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"


def read_input():
    global PAIRS, PACKETS

    with open(BIG_IN) as f:
        lines = f.readlines()

    pair = []
    for line in lines:
        if not line.isspace():
            pair.append(ast.literal_eval(line[:-1]))
            PACKETS.append(ast.literal_eval(line[:-1]))
        else:
            PAIRS.append((pair[0], pair[1]))
            pair = []

    PACKETS.append([[2]])
    PACKETS.append([[6]])


def is_right_order(left, right):
    if (len(left) == 0) and (len(right) > 0):
        return 1
    elif (len(left) > 0) and (len(right) == 0):
        return -1

    i = 0
    j = 0

    for i, j in zip(range((len(left))), range((len(right)))):
        if (type(left[i]) == int) and (type(right[j]) == int):
            if left[i] > right[j]:
                return -1
            elif left[i] < right[j]:
                return 1
        else:
            new_left = left[i] if type(left[i]) == list else [left[i]]
            new_right = right[j] if type(right[j]) == list else [right[j]]

            is_right = is_right_order(new_left, new_right)

            if is_right == -1:
                return -1
            elif is_right == 1:
                return 1

    if (i == (len(left) - 1)) and (j != (len(right) - 1)):
        return 1
    elif (i != (len(left) - 1)) and (j == (len(right) - 1)):
        return -1

    return 0


def solve_task1():
    i = 1
    indices = []

    for pair in PAIRS:
        is_right = is_right_order(pair[0], pair[1])

        if (is_right == 1) or (is_right == 0):
            indices.append(i)

        i += 1

    return sum(indices)


def solve_task2():
    global PACKETS

    PACKETS.sort(key=functools.cmp_to_key(is_right_order), reverse=True)

    index1 = PACKETS.index([[2]]) + 1
    index2 = PACKETS.index([[6]]) + 1

    return index1 * index2


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
