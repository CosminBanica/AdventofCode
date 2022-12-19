[MINUS, PLUS, L, STICK, POINT] = [0, 1, 2, 3, 4]


class Cave:
    def __init__(self, depth=1000, width=7, jet=""):
        self.depth = depth
        self.width = width
        self.cave = [['.' for _ in range(width)] for _ in range(depth)]
        self.spawn_height = 4
        self.jet = jet
        self.current_jet = 0

    def get_spawn_y(self):
        return self.depth - self.spawn_height

    def __repr__(self):
        cave_repr = ""

        for i in range(len(self.cave)):
            if i >= self.get_spawn_y():
                cave_repr += "".join(self.cave[i]) + "\n"

        return cave_repr

    def __getitem__(self, key):
        return self.cave[key]

    def push_minus_right(self, rock):
        if self[rock.y][rock.max_x() + 1] != '.':
            return

        rock.move_right()

    def push_minus_left(self, rock):
        if self[rock.y][rock.min_x() - 1] != '.':
            return

        rock.move_left()

    def push_plus_right(self, rock):
        if self[rock.y - 1][rock.max_x() + 1] != '.':
            return

        if self[rock.y][rock.x + 1] != '.':
            return

        if self[rock.y - 2][rock.x + 1] != '.':
            return

        rock.move_right()

    def push_plus_left(self, rock):
        if self[rock.y - 1][rock.min_x() - 1] != '.':
            return

        if self[rock.y][rock.x - 1] != '.':
            return

        if self[rock.y - 2][rock.x - 1] != '.':
            return

        rock.move_left()

    def push_l_right(self, rock):
        if self[rock.y - 1][rock.max_x() + 1] != '.':
            return

        if self[rock.y][rock.max_x() + 1] != '.':
            return

        if self[rock.y - 2][rock.max_x() + 1] != '.':
            return

        rock.move_right()

    def push_l_left(self, rock):
        if self[rock.y - 1][rock.x + 1] != '.':
            return

        if self[rock.y][rock.min_x() - 1] != '.':
            return

        if self[rock.y - 2][rock.x + 1] != '.':
            return

        rock.move_left()

    def push_stick_right(self, rock):
        if self[rock.y - 1][rock.max_x() + 1] != '.':
            return

        if self[rock.y - 2][rock.max_x() + 1] != '.':
            return

        if self[rock.y - 3][rock.max_x() + 1] != '.':
            return

        if self[rock.y][rock.max_x() + 1] != '.':
            return

        rock.move_right()

    def push_stick_left(self, rock):
        if self[rock.y - 1][rock.x - 1] != '.':
            return

        if self[rock.y - 2][rock.x - 1] != '.':
            return

        if self[rock.y - 3][rock.x - 1] != '.':
            return

        if self[rock.y][rock.x - 1] != '.':
            return

        rock.move_left()

    def push_point_right(self, rock):
        if self[rock.y][rock.max_x() + 1] != '.':
            return

        if self[rock.y - 1][rock.max_x() + 1] != '.':
            return

        rock.move_right()

    def push_point_left(self, rock):
        if self[rock.y][rock.x - 1] != '.':
            return

        if self[rock.y - 1][rock.x - 1] != '.':
            return

        rock.move_left()

    def push_rock(self, rock):
        if self.jet[self.current_jet] == '>' and (rock.max_x() < self.width - 1):
            if rock.rock_type == MINUS:
                self.push_minus_right(rock)
            elif rock.rock_type == PLUS:
                self.push_plus_right(rock)
            elif rock.rock_type == L:
                self.push_l_right(rock)
            elif rock.rock_type == STICK:
                self.push_stick_right(rock)
            elif rock.rock_type == POINT:
                self.push_point_right(rock)
        elif rock.min_x() > 0:
            if rock.rock_type == MINUS:
                self.push_minus_left(rock)
            elif rock.rock_type == PLUS:
                self.push_plus_left(rock)
            elif rock.rock_type == L:
                self.push_l_left(rock)
            elif rock.rock_type == STICK:
                self.push_stick_left(rock)
            elif rock.rock_type == POINT:
                self.push_point_left(rock)
        self.current_jet = (self.current_jet + 1) % len(self.jet)

    def place_minus(self, rock):
        for i in range(rock.min_x(), rock.max_x() + 1):
            self[rock.y][i] = '#'

    def place_plus(self, rock):
        self[rock.y][rock.x] = '#'
        self[rock.y - 1][rock.x - 1] = '#'
        self[rock.y - 1][rock.x + 1] = '#'
        self[rock.y - 1][rock.x] = '#'
        self[rock.y - 2][rock.x] = '#'

    def place_l(self, rock):
        self[rock.y][rock.x] = '#'
        self[rock.y - 1][rock.max_x()] = '#'
        self[rock.y - 2][rock.max_x()] = '#'
        self[rock.y][rock.x + 1] = '#'
        self[rock.y][rock.x + 2] = '#'

    def place_stick(self, rock):
        self[rock.y][rock.x] = '#'
        self[rock.y - 1][rock.x] = '#'
        self[rock.y - 2][rock.x] = '#'
        self[rock.y - 3][rock.x] = '#'

    def place_point(self, rock):
        self[rock.y][rock.x] = '#'
        self[rock.y][rock.x + 1] = '#'
        self[rock.y - 1][rock.x] = '#'
        self[rock.y - 1][rock.x + 1] = '#'

    def place_rock(self, rock):
        if rock.min_y() < (self.get_spawn_y() + 3):
            self.spawn_height += (self.get_spawn_y() + 3) - rock.min_y()
        if rock.rock_type == MINUS:
            self.place_minus(rock)
        elif rock.rock_type == PLUS:
            self.place_plus(rock)
        elif rock.rock_type == L:
            self.place_l(rock)
        elif rock.rock_type == STICK:
            self.place_stick(rock)
        elif rock.rock_type == POINT:
            self.place_point(rock)

    def lower_minus(self, rock):
        for i in range(rock.min_x(), rock.max_x() + 1):
            if self[rock.y + 1][i] != '.':
                return

        rock.move_down()

    def lower_plus(self, rock):
        if self[rock.y + 1][rock.x] != '.':
            return

        if self[rock.y][rock.x - 1] != '.':
            return

        if self[rock.y][rock.x + 1] != '.':
            return

        rock.move_down()

    def lower_l(self, rock):
        for i in range(rock.min_x(), rock.max_x() + 1):
            if self[rock.y + 1][i] != '.':
                return

        rock.move_down()

    def lower_stick(self, rock):
        if self[rock.y + 1][rock.x] != '.':
            return

        rock.move_down()

    def lower_point(self, rock):
        if self[rock.y + 1][rock.x] != '.':
            return

        if self[rock.y + 1][rock.x + 1] != '.':
            return

        rock.move_down()

    def lower_rock(self, rock):
        if rock.max_y() >= self.depth - 1:
            return

        if rock.rock_type == MINUS:
            self.lower_minus(rock)
        elif rock.rock_type == PLUS:
            self.lower_plus(rock)
        elif rock.rock_type == L:
            self.lower_l(rock)
        elif rock.rock_type == STICK:
            self.lower_stick(rock)
        elif rock.rock_type == POINT:
            self.lower_point(rock)

    def can_lower_rock(self, rock):
        if rock.max_y() >= self.depth - 1:
            return False

        if rock.rock_type == MINUS:
            for i in range(rock.min_x(), rock.max_x() + 1):
                if self[rock.y + 1][i] != '.':
                    return False
        elif rock.rock_type == PLUS:
            if self[rock.y + 1][rock.x] != '.':
                return False

            if self[rock.y][rock.x - 1] != '.':
                return False

            if self[rock.y][rock.x + 1] != '.':
                return False
        elif rock.rock_type == L:
            for i in range(rock.min_x(), rock.max_x() + 1):
                if self[rock.y + 1][i] != '.':
                    return False
        elif rock.rock_type == STICK:
            if self[rock.y + 1][rock.x] != '.':
                return False
        elif rock.rock_type == POINT:
            if self[rock.y + 1][rock.x] != '.':
                return False

            if self[rock.y + 1][rock.x + 1] != '.':
                return False

        return True


class Rock:
    def __init__(self, spawn_y, rock_type):
        self.rock_type = rock_type
        self.y = spawn_y

        if rock_type == MINUS:
            self.x = 2
            self.shape = [['@', '@', '@', '@']]
            self.dist_to_max_x = 3
            self.dist_to_min_x = 0
        elif rock_type == PLUS:
            self.x = 3
            self.shape = [['.', '@', '.'], ['@', '@', '@'], ['.', '@', '.']]
            self.dist_to_max_x = 1
            self.dist_to_min_x = 1
        elif rock_type == L:
            self.x = 2
            self.shape = [['.', '.', '@'], ['.', '.', '@'], ['@', '@', '@']]
            self.dist_to_max_x = 2
            self.dist_to_min_x = 0
        elif rock_type == STICK:
            self.x = 2
            self.shape = [['@'], ['@'], ['@'], ['@']]
            self.dist_to_max_x = 0
            self.dist_to_min_x = 0
        elif rock_type == POINT:
            self.x = 2
            self.shape = [['@', '@'], ['@', '@']]
            self.dist_to_max_x = 1
            self.dist_to_min_x = 0
        else:
            raise ValueError("Invalid rock type")

    def __repr__(self):
        rock_repr = ""

        for i in range(len(self.shape)):
            rock_repr += "".join(self.shape[i]) + "\n"

        return rock_repr

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def move_down(self):
        self.y += 1

    def max_x(self):
        return self.x + self.dist_to_max_x

    def min_x(self):
        return self.x - self.dist_to_min_x

    def max_y(self):
        return self.y

    def min_y(self):
        return self.y - len(self.shape)
