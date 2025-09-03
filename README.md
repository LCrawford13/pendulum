# Pendulum
This repository contains code allowing the simulation of a simple pendulum over one full period of motion. The data can then also be used to produce an animation of the simulation. The length, gravitational acceleration, initial angle, initial angular velocity and the position of the pivot can all be specified, all only on a 2D plane.

## Table of Contents

- [Pendulum](#pendulum)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [Testing](#testing)
  - [Contributing](#contributing)
  - [Contacts](#contacts)
  - [Licence](#licence)

## Setup

To install, clone the repository:
```shell
git clone https://github.com/LCrawford13/pendulum.git
```

Use poetry on the directory of the clone:
```shell
poetry install
```

If getting exit code status 9009, run this:
```shell
poetry config virtualenvs.use-poetry-python true
```

Note: I am unaware if this will work on OS's other than Windows.

### Prerequisites

Python (>=3.13.5) is required.

Poetry is required, for the automatic installation of dependencies, https://python-poetry.org/docs/#installing-with-the-official-installer. 

If saving animations to mp4 files, then ffmpeg is needed: https://ffmpeg.org/download.html#build-windows.

## Usage

Run via an IDE, any python supported IDE will work, when running the animation should appear in a new window. However, this is not ideal, as this currently runs the animation too slowly, it's best to save it as an mp4 instead, which has no issues.

The file to run is src/main.py, it has a text-based user interface, or if desired, you can just change values in the editor.

Running from the terminal can be done, via `poetry run py src/main.py`. However, this method can't save the animation as a file.

### Testing

Pytest is used for testing, just run `poetry run pytest` at the project directory, this will run all unit tests.

## Contributing

Contributions aren't excepted at this time.

## Contacts

Github: [LCrawford13](https://github.com/LCrawford13)

Email: lukeaubyncrawford@gmail.com

## Licence

Under MIT licence.
