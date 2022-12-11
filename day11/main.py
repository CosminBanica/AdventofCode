MONKEYS = []
MOD = 1
NR_MONKE = 8


def get_monkey_function(x):
    operator = x[:-1].split(" ")[-2]
    nr = x[:-1].split(" ")[-1]
    if operator == "+":
        if nr == "old":
            return lambda y: y + y
        else:
            return lambda y, z=nr: y + int(z)
    else:
        if nr == "old":
            return lambda y: y * y
        else:
            return lambda y, z=nr: y * int(z)


def read_input(f):
    global MONKEYS, MOD

    for i in range(NR_MONKE):
        monkey = {}

        # get monkey number
        x = f.readline()
        monkey['nr'] = int(x[:-1].replace(":", "").split(" ")[1])

        # get monkey items
        x = f.readline()
        items = x[:-1].replace(",", "").split(" ")[4:]
        int_items = []
        for item in items:
            int_items.append(int(item))
        monkey["items"] = int_items

        # get monkey function
        x = f.readline()
        monkey['fnc'] = get_monkey_function(x)

        # get monkey condition
        x = f.readline()
        mod = int(x[:-1].split(" ")[-1])
        x = f.readline()
        true = int(x[:-1].split(" ")[-1])
        x = f.readline()
        false = int(x[:-1].split(" ")[-1])
        monkey["if"] = lambda y, t=true, fals=false, m=mod: t if y % m == 0 else fals

        # prepare MOD
        MOD *= mod

        # initialize monkey number of inspects
        monkey["inspects"] = 0
        x = f.readline()

        # add monkey to MONKEY list
        MONKEYS.append(monkey)


def solve(name):
    global MONKEYS
    f = open(name, "r")

    read_input(f)

    for i in range(10000):
        for j in range(len(MONKEYS)):
            for item in MONKEYS[j]["items"]:
                # calculate new item worry
                new_item = MONKEYS[j]["fnc"](item) % MOD

                # find target for item
                target = MONKEYS[j]["if"](new_item)

                # send item to target
                MONKEYS[target]["items"].append(new_item)

                # increment number of times this monkey has evaluated
                MONKEYS[j]["inspects"] = MONKEYS[j]["inspects"] + 1

            # this monkey has no items now
            MONKEYS[j]["items"] = []

    # sort monkeys by number of times they inspected
    sorted_monkeys = sorted(MONKEYS, key=lambda y: y['inspects'])

    # get result by multyplying the two monkeys who inspected the most
    output = sorted_monkeys[len(sorted_monkeys) - 1]["inspects"] * sorted_monkeys[len(sorted_monkeys) - 2]["inspects"]

    return output


if __name__ == '__main__':
    result = solve('input.txt')

    print('result:')
    print(result)
