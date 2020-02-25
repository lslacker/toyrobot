from enum import Enum

class Coordinator:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, direction):
        coord = direction.value[0]
        return Coordinator(self.x + coord.x, self.y + coord.y)

    def __str__(self):
        return '<{}({}, {})>'.format(self.__class__.__name__, self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, coord):
        return self.x == coord.x and self.y == coord.y


class Direction(Enum):
    EAST = Coordinator(1, 0), 'NORTH', 'SOUTH'
    WEST = Coordinator(-1, 0), 'SOUTH', 'NORTH'
    NORTH = Coordinator(0, 1), 'WEST', 'EAST'
    SOUTH = Coordinator(0, -1), 'EAST', 'WEST'

    @classmethod
    def from_name(cls, n):
        any_matches = (x for x in cls if x.name == n)
        return next(any_matches, None)

    def left(self):
        return self.from_name(self.value[1])

    def right(self):
        return self.from_name(self.value[2])


class RobotContext:
    place_is_already_executed = False

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.coord = None
        self.direction = None
    
    def valid_move(self):
        new_coord = self.coord + self.direction
        return new_coord.x <= self.columns and new_coord.y <= self.rows

    def __str__(self):
        return 'Output: {},{},{}'.format(self.coord.x, self.coord.y, self.direction.name)

    