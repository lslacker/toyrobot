import pytest
import robot

@pytest.mark.parametrize("x,y,direction,expected_x, expected_y", 
[(0, 0, 'EAST', 1, 0), 
 (1, 1, 'WEST', 0, 1), 
 (5, 5, 'NORTH', 5, 6), 
 (2, 3, 'SOUTH', 2, 2)])
def test_adding_point_with_direction(x, y, direction, expected_x, expected_y):
    p = robot.Coordinator(x, y)
    d = robot.Direction.from_name(direction)
    expected_p = robot.Coordinator(expected_x, expected_y)
    new_p = p + d
    assert new_p == expected_p


@pytest.mark.parametrize("from_direction, left_or_right, expected", 
[('EAST', 'left', 'NORTH')
,('EAST', 'right', 'SOUTH')
,('SOUTH', 'right', 'WEST')
,('NORTH', 'left', 'WEST')])
def test_turning_direction(from_direction, left_or_right, expected):
    from_direction = robot.Direction.from_name(from_direction)
    expected_direction = robot.Direction.from_name(expected)

    if left_or_right == 'left':
        from_direction = from_direction.left()
    else:
        from_direction = from_direction.right()
    
    assert from_direction == expected_direction