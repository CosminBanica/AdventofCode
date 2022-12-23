from solver_template import solver_template

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
INPUT = SMALL_IN if DEBUG else BIG_IN
NORTH, SOUTH, WEST, EAST = 0, 1, 2, 3
ROUNDS = 10


def read_input():
    elves = []
    ground = []

    with open(INPUT) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        ground_line = []
        for j, char in enumerate(line[:-1]):
            ground_line.append(char)
            if char == '#':
                elves.append({'pos': (i, j), 'consideration_order': [NORTH, SOUTH, WEST, EAST]})
        ground.append(ground_line)

    return ground, elves


def add_new_ground_line_at_top(ground, elves, considerations):
    new_ground_line = ['.'] * len(ground[0])
    ground.insert(0, new_ground_line)
    for elf in elves:
        elf['pos'] = (elf['pos'][0] + 1, elf['pos'][1])
    for i in range(len(considerations)):
        considerations[i] = (considerations[i][0] + 1, considerations[i][1])


def add_new_ground_column_at_left(ground, elves, considerations):
    for i in range(len(ground)):
        ground[i].insert(0, '.')
    for elf in elves:
        elf['pos'] = (elf['pos'][0], elf['pos'][1] + 1)
    for i in range(len(considerations)):
        considerations[i] = (considerations[i][0], considerations[i][1] + 1)


def is_elf_far_enough(elf, elves):
    # If no other elf is in the eight positions around the elf, return True
    for other_elf in elves:
        if other_elf == elf:
            continue
        if abs(elf['pos'][0] - other_elf['pos'][0]) <= 1 and abs(elf['pos'][1] - other_elf['pos'][1]) <= 1:
            return False

    return True


def solve_task1(puzzle_data):
    ground, elves = puzzle_data

    for _ in range(10):
        # # print ground
        # for ground_line in ground:
        #     print(''.join(ground_line))
        # print()
        considerations = []

        # Elves are considering where to move
        for k, elf in enumerate(elves):
            i, j = elf['pos']

            elf_should_move = not is_elf_far_enough(elf, elves)

            if elf_should_move:
                for consideration in elf['consideration_order']:
                    if consideration == NORTH:
                        if i == 0:
                            i += 1
                            add_new_ground_line_at_top(ground, elves, considerations)
                            considerations.append((i - 1, j))
                            break
                        else:
                            if (j - 1) < 0:
                                if ground[i - 1][j] == '.' and ground[i - 1][j + 1] == '.':
                                    considerations.append((i - 1, j))
                                    break
                            elif (j + 1) >= len(ground[0]):
                                if ground[i - 1][j] == '.' and ground[i - 1][j - 1] == '.':
                                    considerations.append((i - 1, j))
                                    break
                            else:
                                if ground[i - 1][j] == '.' and ground[i - 1][j - 1] == '.' and ground[i - 1][j + 1] == '.':
                                    considerations.append((i - 1, j))
                                    break
                    elif consideration == SOUTH:
                        if i == len(ground) - 1:
                            ground.append(['.'] * len(ground[0]))
                            considerations.append((i + 1, j))
                            break
                        else:
                            if (j - 1) < 0:
                                if ground[i + 1][j] == '.' and ground[i + 1][j + 1] == '.':
                                    considerations.append((i + 1, j))
                                    break
                            elif (j + 1) >= len(ground[0]):
                                if ground[i + 1][j] == '.' and ground[i + 1][j - 1] == '.':
                                    considerations.append((i + 1, j))
                                    break
                            else:
                                if ground[i + 1][j] == '.' and ground[i + 1][j - 1] == '.' and ground[i + 1][j + 1] == '.':
                                    considerations.append((i + 1, j))
                                    break
                    elif consideration == WEST:
                        if j == 0:
                            j += 1
                            add_new_ground_column_at_left(ground, elves, considerations)
                            considerations.append((i, j - 1))
                            break
                        else:
                            if (i - 1) < 0:
                                if ground[i][j - 1] == '.' and ground[i + 1][j - 1] == '.':
                                    considerations.append((i, j - 1))
                                    break
                            elif (i + 1) >= len(ground):
                                if ground[i][j - 1] == '.' and ground[i - 1][j - 1] == '.':
                                    considerations.append((i, j - 1))
                                    break
                            else:
                                if ground[i][j - 1] == '.' and ground[i - 1][j - 1] == '.' and ground[i + 1][j - 1] == '.':
                                    considerations.append((i, j - 1))
                                    break
                    elif consideration == EAST:
                        if j == len(ground[0]) - 1:
                            for c in range(len(ground)):
                                ground[c].append('.')
                            considerations.append((i, j + 1))
                            break
                        else:
                            if (i - 1) < 0:
                                if ground[i][j + 1] == '.' and ground[i + 1][j + 1] == '.':
                                    considerations.append((i, j + 1))
                                    break
                            elif (i + 1) >= len(ground):
                                if ground[i][j + 1] == '.' and ground[i - 1][j + 1] == '.':
                                    considerations.append((i, j + 1))
                                    break
                            else:
                                if ground[i][j + 1] == '.' and ground[i - 1][j + 1] == '.' and ground[i + 1][j + 1] == '.':
                                    considerations.append((i, j + 1))
                                    break

            if len(considerations) != k + 1:
                considerations.append((-99999, -99999))
            elf['consideration_order'].append(elf['consideration_order'].pop(0))

        # Elves are moving if their consideration doesn't coincide with another elf's consideration
        for k, elf in enumerate(elves):
            i, j = elf['pos']
            new_i, new_j = considerations[k]

            if not (new_i < 0 and new_j < 0):
                if (new_i, new_j) not in considerations[:k] + considerations[k + 1:]:
                    ground[new_i][new_j] = '#'
                    ground[i][j] = '.'
                    elf['pos'] = (new_i, new_j)

    # remove edge rows and columns if they consist entirely of empty space
    while all([ground[0][j] == '.' for j in range(len(ground[0]))]):
        ground.pop(0)
    while all([ground[-1][j] == '.' for j in range(len(ground[0]))]):
        ground.pop()
    while all([ground[i][0] == '.' for i in range(len(ground))]):
        for i in range(len(ground)):
            ground[i].pop(0)
    while all([ground[i][-1] == '.' for i in range(len(ground))]):
        for i in range(len(ground)):
            ground[i].pop()

    # print ground
    for ground_line in ground:
        print(''.join(ground_line))
    print()

    # count empty tiles in ground
    empty_tiles = 0
    for ground_line in ground:
        for tile in ground_line:
            if tile == '.':
                empty_tiles += 1

    return empty_tiles


def solve_task2(puzzle_data):
    global ROUNDS
    ground, elves = puzzle_data

    while True:
        # # print ground
        # for ground_line in ground:
        #     print(''.join(ground_line))
        # print()
        considerations = []

        # Elves are considering where to move
        for k, elf in enumerate(elves):
            i, j = elf['pos']

            elf_should_move = not is_elf_far_enough(elf, elves)

            if elf_should_move:
                for consideration in elf['consideration_order']:
                    if consideration == NORTH:
                        if i == 0:
                            i += 1
                            add_new_ground_line_at_top(ground, elves, considerations)
                            considerations.append((i - 1, j))
                            break
                        else:
                            if (j - 1) < 0:
                                if ground[i - 1][j] == '.' and ground[i - 1][j + 1] == '.':
                                    considerations.append((i - 1, j))
                                    break
                            elif (j + 1) >= len(ground[0]):
                                if ground[i - 1][j] == '.' and ground[i - 1][j - 1] == '.':
                                    considerations.append((i - 1, j))
                                    break
                            else:
                                if ground[i - 1][j] == '.' and ground[i - 1][j - 1] == '.' and ground[i - 1][
                                    j + 1] == '.':
                                    considerations.append((i - 1, j))
                                    break
                    elif consideration == SOUTH:
                        if i == len(ground) - 1:
                            ground.append(['.'] * len(ground[0]))
                            considerations.append((i + 1, j))
                            break
                        else:
                            if (j - 1) < 0:
                                if ground[i + 1][j] == '.' and ground[i + 1][j + 1] == '.':
                                    considerations.append((i + 1, j))
                                    break
                            elif (j + 1) >= len(ground[0]):
                                if ground[i + 1][j] == '.' and ground[i + 1][j - 1] == '.':
                                    considerations.append((i + 1, j))
                                    break
                            else:
                                if ground[i + 1][j] == '.' and ground[i + 1][j - 1] == '.' and ground[i + 1][
                                    j + 1] == '.':
                                    considerations.append((i + 1, j))
                                    break
                    elif consideration == WEST:
                        if j == 0:
                            j += 1
                            add_new_ground_column_at_left(ground, elves, considerations)
                            considerations.append((i, j - 1))
                            break
                        else:
                            if (i - 1) < 0:
                                if ground[i][j - 1] == '.' and ground[i + 1][j - 1] == '.':
                                    considerations.append((i, j - 1))
                                    break
                            elif (i + 1) >= len(ground):
                                if ground[i][j - 1] == '.' and ground[i - 1][j - 1] == '.':
                                    considerations.append((i, j - 1))
                                    break
                            else:
                                if ground[i][j - 1] == '.' and ground[i - 1][j - 1] == '.' and ground[i + 1][
                                    j - 1] == '.':
                                    considerations.append((i, j - 1))
                                    break
                    elif consideration == EAST:
                        if j == len(ground[0]) - 1:
                            for c in range(len(ground)):
                                ground[c].append('.')
                            considerations.append((i, j + 1))
                            break
                        else:
                            if (i - 1) < 0:
                                if ground[i][j + 1] == '.' and ground[i + 1][j + 1] == '.':
                                    considerations.append((i, j + 1))
                                    break
                            elif (i + 1) >= len(ground):
                                if ground[i][j + 1] == '.' and ground[i - 1][j + 1] == '.':
                                    considerations.append((i, j + 1))
                                    break
                            else:
                                if ground[i][j + 1] == '.' and ground[i - 1][j + 1] == '.' and ground[i + 1][
                                    j + 1] == '.':
                                    considerations.append((i, j + 1))
                                    break

            if len(considerations) != k + 1:
                considerations.append((-99999, -99999))
            elf['consideration_order'].append(elf['consideration_order'].pop(0))

        # Elves are moving if their consideration doesn't coincide with another elf's consideration
        any_elf_moved = False
        for k, elf in enumerate(elves):
            i, j = elf['pos']
            new_i, new_j = considerations[k]

            if not (new_i < 0 and new_j < 0):
                any_elf_moved = True
                if (new_i, new_j) not in considerations[:k] + considerations[k + 1:]:
                    ground[new_i][new_j] = '#'
                    ground[i][j] = '.'
                    elf['pos'] = (new_i, new_j)

        ROUNDS += 1
        print(ROUNDS)

        if not any_elf_moved:
            break

    # print ground
    for ground_line in ground:
        print(''.join(ground_line))
    print()

    return ROUNDS


if __name__ == '__main__':
    data = read_input()
    task1_data = data
    task2_data = data
    solver_template(solve_task1=solve_task1, solve_task2=solve_task2, task1_args=task1_data, task2_args=task2_data)
