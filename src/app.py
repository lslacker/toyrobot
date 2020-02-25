import sys
import argparse
import logging
from enum import Enum
from pyparsing import Literal, oneOf, Regex

logger = logging.getLogger(__name__)

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


def getDirection(t: str):
    any_matches = [x for x in Direction if x.name == t[0]]
    return any_matches[0]


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

    def __init__(self, rows=5, columns=5):
        self.rows = 5
        self.columns = 5
        self.coord = None
        self.direction = None
    
    def valid_move(self):
        new_coord = self.coord + self.direction
        
        return new_coord.x <= self.columns and new_coord.y <= self.rows

    def __str__(self):
        return 'Output: {},{},{}'.format(self.coord.x, self.coord.y, self.direction.name)


REGISTERED_CLASSES = {}

def registered_class(cls):
    REGISTERED_CLASSES[cls.__name__.replace('Command', '').lower()] = cls
    return cls

class Command():
    
    def __init__(self, tokens):
        self.__dict__.update(tokens.asDict())

    def exec(self, context):
        self._do_exec(context)

def setCommand(tokens):
    lookup = tokens.asDict()
    cls = REGISTERED_CLASSES.get(lookup['command'].lower())
    return cls(tokens)

@registered_class
class PlaceCommand(Command):

    def _do_exec(self, context):
        context.coord = self.at
        context.direction = self.direction
        context.place_is_already_executed = True

@registered_class
class MoveCommand(Command):
    def _do_exec(self, context):
        if context.place_is_already_executed and context.valid_move():
            context.coord = context.coord + context.direction

@registered_class
class ReportCommand(Command):
    def _do_exec(self, context):
        if context.place_is_already_executed:
            print(context)

@registered_class
class LeftCommand(Command):
    def _do_exec(self, context):
        if context.place_is_already_executed:
            context.direction = context.direction.left()

@registered_class
class RightCommand(Command):
    def _do_exec(self, context):
        if context.place_is_already_executed:
            context.direction = context.direction.right()

number = Regex(r'\d').setParseAction(lambda t: int(t[0]))
comma = Literal(',')
coordinator = (number('x') + comma.suppress() + number('y')).setParseAction(lambda t: Coordinator(t[0], t[1]))("at")
placeDefn = Literal("PLACE")("command") + coordinator + comma.suppress() + oneOf("NORTH SOUTH EAST WEST").setParseAction(lambda t: Direction.from_name(t[0]))("direction")
commandDefn = placeDefn | oneOf("MOVE LEFT RIGHT REPORT")("command")
commandDefn.setParseAction(setCommand)


def consoleUI():
    parser = argparse.ArgumentParser(description='Simulation of a toy robot moving on a square table top,')
    parser.add_argument('infile', default=sys.stdin, type=argparse.FileType('r'), nargs='?')
    
    a = parser.parse_args()
    robot = RobotContext(5, 5)

    for line in a.infile:
        print(line.strip())
        command = commandDefn.parseString(line)
        
        command[0].exec(robot)

if __name__ == '__main__':
    
    consoleUI()
    