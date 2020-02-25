# ToyRobot

[![Build Status](https://travis-ci.com/lslacker/toyrobot.svg?branch=master)](https://travis-ci.com/lslacker/toyrobot)

## Build a run using Docker
- Clone the repository, change to project directory
- Update sample.txt
- $> docker build -t . -name toyrobot
- $> docker run -it --rm toyrobot  python app.py sample.txt

# Build a run using virtual environment (Python 3.6+)
  - Clone the repository, change to project directory
  - Create new environment: $> python -m venv env
  - $> source env/bin/activate
  - $> pip install -r requirements.txt
  - $> python -m pytest
  - $> python app.py sample.txt    # read from file
      OR $> python app.py    # read from standard input
