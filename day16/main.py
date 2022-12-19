import re
import time

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
INPUT = SMALL_IN if DEBUG else BIG_IN
STORE_DICT = {}
STEPS = {}


class Valve:
    def __init__(self, name, flow_rate: int, connections):
        self.name = name
        self.flow_rate = flow_rate
        self.connections = connections

    def __repr__(self) -> str:
        return f"Valve('{self.name}', {self.flow_rate}, {self.connections})"

    def __eq__(self, __o: object) -> bool:
        return (self.name == __o.name
                and self.flow_rate == __o.flow_rate
                and self.connections == __o.connections)


def read_input():
    global STORE_DICT, STEPS

    prog = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); '
                      r'tunnels? leads? to valves? ((([A-Z]{2}), )*([A-Z]{2}))')

    with open(INPUT) as f:
        for line in f:
            match = prog.match(line)
            if match:
                name = match.group(1)
                flow_rate = int(match.group(2))
                connections = set(match.group(3).split(', '))
                valve = Valve(name, flow_rate, connections)
                STORE_DICT[name] = valve

    # Floyd-Warshall Algorithm for steps between nodes (valves)
    STEPS = {x: {y: 1 if y in STORE_DICT[x].connections else float('inf') for y in STORE_DICT} for x in STORE_DICT}
    for k in STEPS:
        for i in STEPS:
            for j in STEPS:
                STEPS[i][j] = min(STEPS[i][j], STEPS[i][k] + STEPS[k][j])


def traveling_elf(valves, last_valve, time_remaining, state_machine, state, flow, answer):
    answer[state] = max(answer.get(state, 0), flow)

    for valve in valves:
        minutes = time_remaining - STEPS[last_valve][valve] - 1

        # Bit-masking for state. Each bit represents valve
        if (state_machine[valve] & state) or (minutes <= 0):
            # print("skipping ", valve, " because state_machine[valve] & state ", state_machine[valve] & state, " or minutes <= 0 ", minutes <= 0)
            continue

        # Recursion - add this valve to the state. Add this valve to the flow
        # print("adding ", valve, " to state ", state, " and flow ", flow)
        traveling_elf(valves, valve, minutes, state_machine,
                      state | state_machine[valve],
                      flow + (minutes * valves[valve].flow_rate),
                      answer)
    return answer


def solve_task1():
    minutes = 30
    valves = {name: valve for (name, valve) in STORE_DICT.items() if valve.flow_rate > 0}
    state_machine = {v: 1 << i for i, v in enumerate(valves)}
    last_valve = 'AA'
    starting_state = 0
    starting_flow = 0
    total_flow = max(traveling_elf(valves, last_valve, minutes,
                                   state_machine, starting_state, starting_flow,
                                   {}).values())
    return total_flow


def solve_task2():
    minutes = 26
    valves = {name: valve for (name, valve) in STORE_DICT.items() if valve.flow_rate > 0}
    state_machine = {v: 1 << i for i, v in enumerate(valves)}
    last_valve = 'AA'
    starting_state = 0
    starting_flow = 0
    paths = traveling_elf(valves, last_valve, minutes,
                          state_machine, starting_state, starting_flow, {})

    total_flow = max(my_val + el_val for k1, my_val in paths.items()
                     for k2, el_val in paths.items() if not k1 & k2)
    return total_flow


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
