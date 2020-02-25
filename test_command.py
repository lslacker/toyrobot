import pytest
import command


@pytest.mark.parametrize("line,expected", 
[('MOVE', 'MoveCommand'),
 ('LEFT', 'LeftCommand'), 
 ('RIGHT', 'RightCommand'),
 ('PLACE 0,  0,  NORTH', 'PlaceCommand'),
 ('PLACE 0,  0,,  NORTH', 'NoActionCommand'),
 ('PLACE', 'NoActionCommand')])
def test_parse_string_as_command(line, expected):
    cmd = command.get_command(line)
    assert expected == cmd.__class__.__name__

