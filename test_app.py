import pytest
import io
import app
from robot import RobotContext

MAX_ROWS = 5
MAX_COLUMNS = 5

@pytest.fixture
def test_robot():
    robot = RobotContext(MAX_ROWS, MAX_COLUMNS)
    return robot

def process(input_commands, test_robot):
    infile = io.StringIO(input_commands)
    outfile = io.StringIO()
    app.process(infile, outfile, test_robot)
    outfile.seek(0)
    val = outfile.getvalue()
    return val

def test_input_command_output_result(test_robot):
    input_commands = '''PLACE 0,0,NORTH
MOVE
REPORT
'''
    expected = '''{}Output: 0,1,NORTH
'''.format(input_commands)

    val = process(input_commands, test_robot)
    
    assert val == expected



def test_robot_commands_not_place(test_robot):
    input_commands = '''MOVE
LEFT
REPORT
'''
    expected = '''{}'''.format(input_commands)

    val = process(input_commands, test_robot)
    
    assert val == expected
    assert test_robot.valid_move() == False
    assert test_robot.place_is_already_executed == False


def test_robot_commands_place_outside(test_robot):
    input_commands = '''PLACE 10,10,NORTH
MOVE
REPORT
'''
    expected = '''{}'''.format(input_commands)

    val = process(input_commands, test_robot)
    
    assert val == expected
    assert test_robot.valid_move() == False
    assert test_robot.place_is_already_executed == False


def test_robot_commands_to_border_staysame_if_outside_boundary(test_robot):
    input_commands = '''PLACE 3,3,NORTH
MOVE
MOVE
MOVE
MOVE
REPORT
'''
    expected = '''{}Output: 3,4,NORTH
'''.format(input_commands)
    assert test_robot.place_is_already_executed == False
    val = process(input_commands, test_robot)
    assert val == expected
    assert test_robot.place_is_already_executed == True


def test_robot_commands_place_outside(test_robot):
    input_commands = '''PLACE 3,3,NORTH
MOVE
MOVE
MOVE
LEFT
MOVE
REPORT
MOVE
MOVE
REPORT
RIGHT
REPORT
INVALID COMMAND
REPORT
'''
    expected = '''PLACE 3,3,NORTH
MOVE
MOVE
MOVE
LEFT
MOVE
REPORT
Output: 2,4,WEST
MOVE
MOVE
REPORT
Output: 0,4,WEST
RIGHT
REPORT
Output: 0,4,NORTH
INVALID COMMAND
REPORT
Output: 0,4,NORTH
'''
    assert test_robot.place_is_already_executed == False
    val = process(input_commands, test_robot)
    assert val == expected
    assert test_robot.place_is_already_executed == True
