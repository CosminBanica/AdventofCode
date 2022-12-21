import re
from solver_template import solver_template

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
INPUT = SMALL_IN if DEBUG else BIG_IN


class Node:
    def __init__(self, value, left_name=None, right_name=None):
        self.value = value
        self.left_name = left_name
        self.right_name = right_name
        self.left = None
        self.right = None

    def __repr__(self):
        if self.left:
            return f"({self.left} {self.value} {self.right})"
        else:
            return f"{self.value}"

    def get_number(self):
        if type(self.value) == int:
            return self.value
        else:
            if self.value == "+":
                return self.left.get_number() + self.right.get_number()
            elif self.value == "*":
                return self.left.get_number() * self.right.get_number()
            elif self.value == "-":
                return self.left.get_number() - self.right.get_number()
            elif self.value == "/":
                return self.left.get_number() / self.right.get_number()

    def left_equals_right(self):
        return self.left.get_number() == self.right.get_number()

    def left_greater_than_right(self):
        return self.left.get_number() > self.right.get_number()


def read_input():
    monkeys = {}

    with open(INPUT) as f:
        lines = f.readlines()

    for line in lines:
        values = line[:-1].replace(":", "").split(" ")
        monkey = values[0]

        if len(values) == 2:
            number = int(values[1])
            monkeys[monkey] = Node(number)
        else:
            operation = values[2]
            left_monkey = values[1]
            right_monkey = values[3]
            monkeys[monkey] = Node(operation, left_monkey, right_monkey)

    for monkey in monkeys:
        if monkeys[monkey].left_name:
            monkeys[monkey].left = monkeys[monkeys[monkey].left_name]
        if monkeys[monkey].right_name:
            monkeys[monkey].right = monkeys[monkeys[monkey].right_name]

    return monkeys


def solve_task1(puzzle_data):
    res = puzzle_data["root"].get_number()

    return res


def solve_task2(puzzle_data):
    puzzle_data["humn"].value = 3403989690001

    while not puzzle_data["root"].left_equals_right():
        greater = puzzle_data["root"].left_greater_than_right()
        if not greater:
            print(puzzle_data["humn"].value)
            break
        puzzle_data["humn"].value += 1

    res = puzzle_data["humn"].value

    return res


if __name__ == '__main__':
    data = read_input()
    solver_template(solve_task1, solve_task2, task1_args=data, task2_args=data)
