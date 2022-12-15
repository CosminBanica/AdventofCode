import re
import time

SMALL_IN = "small_input.txt"
BIG_IN = "input.txt"
DEBUG = False
TARGET_LINE_Y = 10 if DEBUG else 2000000
SENSORS = []
BEACONS = []
TUNING_NR = 4000000
MAX_TARGET_Y = 20 if DEBUG else 4000000
INPUT = SMALL_IN if DEBUG else BIG_IN


def manhattan(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def read_input():
    global SENSORS, BEACONS

    with open(INPUT) as f:
        lines = f.readlines()

    for line in lines:
        if not line.isspace():
            points = re.findall(r'-*\d+', line[:-1])
            sensor = (int(points[0]), int(points[1]))
            beacon = (int(points[2]), int(points[3]))

            distance = manhattan(sensor, beacon)

            if beacon not in BEACONS:
                BEACONS.append(beacon)
            SENSORS.append((sensor, distance))


def add_interval_to_list(left_edge, right_edge, interval_list):
    if interval_list:
        for i in range(len(interval_list)):
            if ((interval_list[i][0] >= (left_edge - 1)) and (interval_list[i][0] <= (right_edge + 1))) or \
                    ((interval_list[i][1] >= (left_edge - 1)) and (interval_list[i][1] <= (right_edge + 1))):
                current_target_line_left = interval_list[i][0]
                current_target_line_right = interval_list[i][1]
                interval_list[i] = (min(current_target_line_left, left_edge), max(current_target_line_right, right_edge))
                break
            elif i == (len(interval_list) - 1):
                interval_list.append((left_edge, right_edge))
    else:
        interval_list.append((left_edge, right_edge))

    return interval_list


def merge_intervals_in_list(interval_list):
    interval_list.sort(key=lambda x: x[0])
    merged_target_line = []

    for interval in interval_list:
        if not merged_target_line:
            merged_target_line.append(interval)
        else:
            last_interval = merged_target_line[-1]
            if interval[0] <= last_interval[1]:
                merged_target_line[-1] = (last_interval[0], max(last_interval[1], interval[1]))
            else:
                merged_target_line.append(interval)

    return merged_target_line


def intersect_intervals(interval_list):
    interval_list.sort(key=lambda x: x[0])
    intersection = ()
    for interval in interval_list:
        if not intersection:
            intersection = interval
        else:
            intersection = (max(intersection[0], interval[0]), min(intersection[1], interval[1]))

    return intersection


def solve_task1(target_y):
    target_intervals = []

    for pair in SENSORS:
        sensor = pair[0]
        distance_to_beacon = pair[1]
        distance_to_target_line = manhattan(sensor, (sensor[0], target_y))

        if distance_to_target_line <= distance_to_beacon:
            sensor_x = sensor[0]
            new_target_edge_left = sensor_x - (distance_to_beacon - distance_to_target_line)
            new_target_edge_right = sensor_x + (distance_to_beacon - distance_to_target_line)

            target_intervals = add_interval_to_list(new_target_edge_left, new_target_edge_right, target_intervals)

    merged_intervals = merge_intervals_in_list(target_intervals)

    # Compute nr of impossible and possible positions for beacons
    impossible_beacons = 0
    possible_beacons = MAX_TARGET_Y + 1
    for merged_interval in merged_intervals:
        impossible_beacons += merged_interval[1] - merged_interval[0] + 1

        if (merged_interval[1] >= 0) and (merged_interval[0] <= MAX_TARGET_Y):
            possible_beacons -= min(merged_interval[1], MAX_TARGET_Y) - max(merged_interval[0], 0) + 1

    # Subtract any observed beacons from computed range
    for beacon in BEACONS:
        if beacon[1] == target_y:
            for merged_interval in merged_intervals:
                if (beacon[0] >= merged_interval[0]) and (beacon[0] <= merged_interval[1]):
                    impossible_beacons -= 1
                    break
                else:
                    if (beacon[0] >= 0) and (beacon[0] <= MAX_TARGET_Y):
                        possible_beacons -= 1

    # Subtract any sensors from computed range
    for sensor in SENSORS:
        if sensor[0][1] == target_y:
            for merged_interval in merged_intervals:
                if (sensor[0][0] >= merged_interval[0]) and (sensor[0][0] <= merged_interval[1]):
                    impossible_beacons -= 1
                    break
                else:
                    if (sensor[0][0] >= 0) and (sensor[0][0] <= MAX_TARGET_Y):
                        possible_beacons -= 1

    return impossible_beacons, merged_intervals, possible_beacons


def solve_task2():
    for i in range(MAX_TARGET_Y + 1):
        print("Solving for y = {}".format(i))
        nr_impossible, impossible_intervals, nr_possible = solve_task1(i)

        if nr_possible > 0:
            valid_intervals = []

            for interval in impossible_intervals:
                if interval[0] > 0:
                    valid_intervals.append((0, interval[0] - 1))
                elif interval[1] < MAX_TARGET_Y:
                    valid_intervals.append((interval[1] + 1, MAX_TARGET_Y))

            if valid_intervals:
                intersection = intersect_intervals(valid_intervals)

                if intersection:
                    print("valid intervals: {}".format(intersection))
                    return intersection[0] * TUNING_NR + i

    return 0


if __name__ == '__main__':
    read_input()

    print("Starting task 1")
    start = time.time()
    result = solve_task1(TARGET_LINE_Y)
    print('Task 1 result:' + str(result[0]))
    end = time.time()
    print("Exec time" + str(end - start))

    print("\nStarting task 2")
    start = time.time()
    result = solve_task2()
    print('Task 2 result:' + str(result))
    end = time.time()
    print("Exec time" + str(end - start))
