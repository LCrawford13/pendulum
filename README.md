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

It's best to run via an IDE, any python supported IDE will work. When running, the animation will appear in a new window. However, this is not ideal, as the pop-up window currently runs the animation too slowly, it's best to save it as an mp4 instead, which has no such issues.

The file to run is src/main.py, it has a text-based user interface, or if desired, you can just change the values in an editor.

Running from the terminal can be done, via `poetry run py src/main.py`, run from the root. However, if saving the animation to a file, then the pop-up window with the animation fails to appear, while if not saving to a file, the pop-up window will appear but the terminal will hang, meaning you will have to restart the terminal to run the program again. It should be noted that the pop-up window has the same issues that running from an IDE has.

Picture of animation pop-up window:

<img width="499" height="578" alt="window" src="https://github.com/user-attachments/assets/4bf0c436-5514-4a6d-9c28-046f82f8cc4a" />

Video of full animation on default settings:

https://github.com/user-attachments/assets/7d327dd5-6e8c-417a-903d-128b8165b4df

### Testing

Pytest is used for testing, just run `poetry run pytest` at the project directory, this will run all unit tests.

## Contributing

Contributions aren't excepted at this time.

## Contacts

Github: [LCrawford13](https://github.com/LCrawford13)

Email: lukeaubyncrawford@gmail.com

## Licence

[Under MIT licence.](LICENCE)
