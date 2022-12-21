import time


def solver_template(solve_task1, solve_task2, **kwargs):
    print("Starting task 1")
    start = time.time()
    result = solve_task1(kwargs["task1_args"])
    print('Task 1 result:' + str(result))
    end = time.time()
    print("Exec time" + str(end - start))

    print("\nStarting task 2")
    start = time.time()
    result = solve_task2(kwargs["task2_args"])
    print('Task 2 result:' + str(result))
    end = time.time()
    print("Exec time" + str(end - start))