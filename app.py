import sys
import argparse
from robot import RobotContext
from command import get_command


MAX_ROWS = 5
MAX_COLUMNS = 5

def process(infile, robot):
    for line in infile:
        print(line.strip())
        cmd = get_command(line)
        cmd.exec(robot)

def consoleUI():
    parser = argparse.ArgumentParser(description='Simulation of a toy robot moving on a square table top,')
    parser.add_argument('infile', default=sys.stdin, type=argparse.FileType('r'), nargs='?')
    
    args = parser.parse_args()
    robot = RobotContext(MAX_ROWS, MAX_COLUMNS)
    process(args.infile, robot)

if __name__ == '__main__':
    consoleUI()
