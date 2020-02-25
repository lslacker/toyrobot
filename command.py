import logging
from robot import Coordinator, Direction
from pyparsing import Literal, oneOf, Regex, OneOrMore, Optional

logger = logging.getLogger(__name__)

REGISTERED_CLASSES = {}

def registered_class(cls):
    """Decorator class to register each command class"""
    REGISTERED_CLASSES[cls.__name__.replace('Command', '').lower()] = cls
    return cls


class Command():
    """Abstract command for inheritance"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def exec(self, context):
        self._do_exec(context)


@registered_class
class PlaceCommand(Command):
    """Command to place robot at certain coordinator"""

    def _do_exec(self, context):
        context.coord = self.at
        if context.valid_move:
            context.direction = self.direction
            context.place_is_already_executed = True


@registered_class
class MoveCommand(Command):
    """Command to move robot based on direction set
    in the place command"""

    def _do_exec(self, context):
        if context.place_is_already_executed and context.valid_move():
            context.coord = context.coord + context.direction

@registered_class
class ReportCommand(Command):
    """Print out current robot coordination, as well as direction"""
    def _do_exec(self, context):
        if context.place_is_already_executed:
            context.outfile.write('{!s}\n'.format(context))

@registered_class
class LeftCommand(Command):
    """Turn robot to left based on current direction"""
    def _do_exec(self, context):
        if context.place_is_already_executed:
            context.direction = context.direction.left()

@registered_class
class RightCommand(Command):
    """Turn robot to right based on current direction"""
    def _do_exec(self, context):
        if context.place_is_already_executed:
            context.direction = context.direction.right()


class NoActionCommand(Command):
    """Do nothing, for unknown commands"""
    def _do_exec(self, context):
        pass


def setCommand(tokens):
    """For each line, we will use information
    parsed from pyparsing, look up for the
    required command in REGISTERED_CLASSES, and
    initialise it"""
    lookup = tokens.asDict()
    cls = REGISTERED_CLASSES.get(lookup['command'].lower())
    a = cls(**lookup)
    return a

number = Regex(r'\d').setParseAction(lambda t: int(t[0]))
comma = Literal(',')
space = Literal(' ')
# PLACE 0,0,NORTH
whitespace = comma + Optional(OneOrMore(space))
coordinator = (number('x') + whitespace.suppress() + number('y')).setParseAction(lambda t: Coordinator(t[0], t[1]))("at")
placeDefn = Literal("PLACE")("command") + coordinator + whitespace.suppress() + oneOf("NORTH SOUTH EAST WEST").setParseAction(lambda t: Direction.from_name(t[0]))("direction")

commandDefn = placeDefn | oneOf("MOVE LEFT RIGHT REPORT")("command")
commandDefn.setParseAction(setCommand)

def get_command(line):
    try:
        return commandDefn.parseString(line)[0]
    except Exception:
        pass
    
    return NoActionCommand()
