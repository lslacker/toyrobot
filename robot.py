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

    def __eq__(self, coord):
        return self.x == coord.x and self.y == coord.y


class Direction(Enum):
    EAST = Coordinator(1, 0), 'NORTH', 'SOUTH'
    WEST = Coordinator(-1, 0), 'SOUTH', 'NORTH'
    NORTH = Coordinator(0, 1), 'WEST', 'EAST'
    SOUTH = Coordinator(0, -1), 'EAST', 'WEST'
    STAYSTILL = Coordinator(0, 0), 'STAYSTILL', 'STAYSTILL'

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
        self.direction = Direction.STAYSTILL
    
    def valid_move(self):
        if self.coord:
            new_coord = self.coord + self.direction
            # not equal as index starts at 0
            return new_coord.x < self.columns and new_coord.y < self.rows
        return False

    def __str__(self):
        return 'Output: {},{},{}'.format(self.coord.x, self.coord.y, self.direction.name)

    