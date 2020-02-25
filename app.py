import sys
import argparse
from robot import RobotContext
from command import get_command

def process(infile, outfile, robot):
    
    robot.outfile = outfile

    for line in infile:
        robot.outfile.write(line.strip())
        robot.outfile.write('\n')
        cmd = get_command(line)
        cmd.exec(robot)
    robot.outfile.close()

def consoleUI():
    parser = argparse.ArgumentParser(description='Simulation of a toy robot moving on a square table top,')
    parser.add_argument('--infile', default=sys.stdin, type=argparse.FileType('r'), nargs='?')
    parser.add_argument('--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--rows', type=int, default=5, help='width of the table in units')
    parser.add_argument('--columns', type=int, default=5, help='length of the table in units')
    args = parser.parse_args()
    robot = RobotContext(args.rows, args.columns)
    process(args.infile, args.outfile, robot)

if __name__ == '__main__':
    consoleUI()
