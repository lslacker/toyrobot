# ToyRobot

[![Build Status](https://travis-ci.com/lslacker/toyrobot.svg?branch=master)](https://travis-ci.com/lslacker/toyrobot)

```
$> python app.py -h

usage: app.py [-h] [--infile [INFILE]] [--outfile [OUTFILE]] [--rows ROWS]
              [--columns COLUMNS]

Simulation of a toy robot moving on a square table top,

optional arguments:
  -h, --help           show this help message and exit
  --infile [INFILE]
  --outfile [OUTFILE]
  --rows ROWS          width of the table in units
  --columns COLUMNS    length of the table in units
```

Please update sample.txt for different set of commands

## APPROACH
- Write a parser, to parse each line into Command object
- Execute each command with Context as a parameter
- Context in this case is a ROBOT, with Table dimension

## Build a run using Docker
- Clone the repository, change to project directory
- Update sample.txt
- $> docker build -t . -name toyrobot
- $> docker run -it --rm toyrobot  python app.py --infile sample.txt

# Build a run using virtual environment (Python 3.6+)
  - Clone the repository, change to project directory
  - Create new environment: $> python -m venv env
  - $> source env/bin/activate
  - $> pip install -r requirements.txt
  - $> python -m pytest
  - $> python app.py --infile sample.txt    # read from file
      OR $> python app.py    # read from standard input
      OR $> python app.py --infile sample.txt --outfile output.txt   # read from file, save to output file

