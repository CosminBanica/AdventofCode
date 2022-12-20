import re
import time

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
INPUT = SMALL_IN if DEBUG else BIG_IN
ARRANGEMENT = []
DECRYPTED_ARRANGEMENT = []
DECRYPTION_KEY = 811589153


class Node:
    def __init__(self, value, prv=None, nxt=None):
        self.value = value
        self.prv = prv
        self.nxt = nxt


def read_input():
    global ARRANGEMENT, DECRYPTED_ARRANGEMENT

    with open(INPUT) as f:
        lines = f.readlines()

    for i in range(len(lines)):
        ARRANGEMENT.append(Node(int(lines[i])))
        DECRYPTED_ARRANGEMENT.append(Node(int(lines[i]) * DECRYPTION_KEY))

    for a, b in zip(ARRANGEMENT, ARRANGEMENT[1:]):
        a.nxt = b
        b.prv = a

    for a, b in zip(DECRYPTED_ARRANGEMENT, DECRYPTED_ARRANGEMENT[1:]):
        a.nxt = b
        b.prv = a

    ARRANGEMENT[-1].nxt = ARRANGEMENT[0]
    ARRANGEMENT[0].prv = ARRANGEMENT[-1]
    DECRYPTED_ARRANGEMENT[-1].nxt = DECRYPTED_ARRANGEMENT[0]
    DECRYPTED_ARRANGEMENT[0].prv = DECRYPTED_ARRANGEMENT[-1]


def mix_numbers(numbers):
    for x in numbers:
        x.prv.nxt = x.nxt
        x.nxt.prv = x.prv

        a, b = x.prv, x.nxt
        move = x.value % (len(ARRANGEMENT) - 1)

        for _ in range(move):
            a = a.nxt
            b = b.nxt

        a.nxt = x
        x.prv = a
        b.prv = x
        x.nxt = b


def solve_task1():
    global ARRANGEMENT
    res = 0

    mix_numbers(ARRANGEMENT)

    for x in ARRANGEMENT:
        if x.value == 0:
            y = x
            for _ in range(3):
                for _ in range(1000):
                    y = y.nxt
                res += y.value
            break

    return res


def solve_task2():
    global DECRYPTED_ARRANGEMENT
    res = 0

    for _ in range(10):
        mix_numbers(DECRYPTED_ARRANGEMENT)

    for x in DECRYPTED_ARRANGEMENT:
        if x.value == 0:
            y = x
            for _ in range(3):
                for _ in range(1000):
                    y = y.nxt
                res += y.value
            break

    return res


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
