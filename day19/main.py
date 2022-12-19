import re
import time

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
INPUT = SMALL_IN if DEBUG else BIG_IN
BLUEPRINTS = []
CURRENT_BLUEPRINT = {}
MAX_GEODE = 0
MAX_ORE = 0
MAX_CLAY = 0
MAX_OBSIDIAN = 0
ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3
OPTIMAL_GEODE = [(t - 1) * t // 2 for t in range(32 + 1)]


def read_input():
    global BLUEPRINTS

    with open(INPUT) as f:
        lines = f.readlines()

    lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]

    for line in lines:
        blueprint_id = line[0]
        ore_robot_ore_cost = line[1]
        clay_robot_ore_cost = line[2]
        obsidian_robot_ore_cost = line[3]
        obsidian_robot_clay_cost = line[4]
        geode_robot_ore_cost = line[5]
        geode_robot_obsidian_cost = line[6]
        BLUEPRINTS.append({"id": blueprint_id,
                           "ore_robot_ore_cost": ore_robot_ore_cost,
                           "clay_robot_ore_cost": clay_robot_ore_cost,
                           "obsidian_robot_ore_cost": obsidian_robot_ore_cost,
                           "obsidian_robot_clay_cost": obsidian_robot_clay_cost,
                           "geode_robot_ore_cost": geode_robot_ore_cost,
                           "geode_robot_obsidian_cost": geode_robot_obsidian_cost})


def dfs(time_left, target, ore_robot, clay_robot, obsidian_robot, geode_robot, ore, clay, obsidian, geode):
    global MAX_GEODE

    if ((target == ORE and ore_robot >= MAX_ORE) or
            (target == CLAY and clay_robot >= MAX_CLAY) or
            (target == OBSIDIAN and (obsidian_robot >= MAX_OBSIDIAN or clay_robot == 0)) or
            (target == GEODE and obsidian_robot == 0) or
            (geode + geode_robot * time_left + OPTIMAL_GEODE[time_left] <= MAX_GEODE)):
        return

    while time_left:
        if target == 0 and ore >= CURRENT_BLUEPRINT["ore_robot_ore_cost"]:
            for target in range(4):
                dfs(time_left - 1, target, ore_robot + 1, clay_robot, obsidian_robot, geode_robot,
                    ore - CURRENT_BLUEPRINT["ore_robot_ore_cost"] + ore_robot, clay + clay_robot,
                    obsidian + obsidian_robot, geode + geode_robot)
            return
        elif target == 1 and ore >= CURRENT_BLUEPRINT["clay_robot_ore_cost"]:
            for target in range(4):
                dfs(time_left - 1, target, ore_robot, clay_robot + 1, obsidian_robot, geode_robot,
                    ore - CURRENT_BLUEPRINT["clay_robot_ore_cost"] + ore_robot, clay + clay_robot,
                    obsidian + obsidian_robot, geode + geode_robot)
            return
        elif target == 2 and ore >= CURRENT_BLUEPRINT["obsidian_robot_ore_cost"] and \
                clay >= CURRENT_BLUEPRINT["obsidian_robot_clay_cost"]:
            for target in range(4):
                dfs(time_left - 1, target, ore_robot, clay_robot, obsidian_robot + 1, geode_robot,
                    ore - CURRENT_BLUEPRINT["obsidian_robot_ore_cost"] + ore_robot,
                    clay - CURRENT_BLUEPRINT["obsidian_robot_clay_cost"] + clay_robot,
                    obsidian + obsidian_robot, geode + geode_robot)
            return
        elif target == 3 and ore >= CURRENT_BLUEPRINT["geode_robot_ore_cost"] and \
                obsidian >= CURRENT_BLUEPRINT["geode_robot_obsidian_cost"]:
            for target in range(4):
                dfs(time_left - 1, target, ore_robot, clay_robot, obsidian_robot, geode_robot + 1,
                    ore - CURRENT_BLUEPRINT["geode_robot_ore_cost"] + ore_robot, clay + clay_robot,
                    obsidian - CURRENT_BLUEPRINT["geode_robot_obsidian_cost"] + obsidian_robot, geode + geode_robot)
            return
        time_left, ore, clay, obsidian, geode = time_left - 1, ore + ore_robot, clay + clay_robot, \
                                                obsidian + obsidian_robot, geode + geode_robot

    MAX_GEODE = max(MAX_GEODE, geode)


def solve_task1():
    global CURRENT_BLUEPRINT, MAX_GEODE, MAX_ORE, MAX_CLAY, MAX_OBSIDIAN
    res = 0

    for blueprint in BLUEPRINTS:
        CURRENT_BLUEPRINT = blueprint
        MAX_GEODE = 0
        MAX_ORE, MAX_CLAY, MAX_OBSIDIAN = max(blueprint["ore_robot_ore_cost"], blueprint["clay_robot_ore_cost"],
                                              blueprint["obsidian_robot_ore_cost"], blueprint["geode_robot_ore_cost"]), \
            blueprint["obsidian_robot_clay_cost"], \
            blueprint["geode_robot_obsidian_cost"]
        for target in range(4):
            dfs(24, target, 1, 0, 0, 0, 0, 0, 0, 0)

        res += blueprint["id"] * MAX_GEODE

    return res


def solve_task2():
    global CURRENT_BLUEPRINT, MAX_GEODE, MAX_ORE, MAX_CLAY, MAX_OBSIDIAN
    res = 1

    for blueprint in BLUEPRINTS[:3]:
        CURRENT_BLUEPRINT = blueprint
        MAX_GEODE = 0
        MAX_ORE, MAX_CLAY, MAX_OBSIDIAN = max(blueprint["ore_robot_ore_cost"], blueprint["clay_robot_ore_cost"],
                                              blueprint["obsidian_robot_ore_cost"], blueprint["geode_robot_ore_cost"]), \
            blueprint["obsidian_robot_clay_cost"], \
            blueprint["geode_robot_obsidian_cost"]
        for target in range(4):
            dfs(32, target, 1, 0, 0, 0, 0, 0, 0, 0)

        res *= MAX_GEODE

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
