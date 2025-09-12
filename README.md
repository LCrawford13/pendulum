# Pendulum
This repository contains code which simulates the motion of a simple pendulum over one full period of motion, it uses the Runge-Kutta algorithim. The data produced can then also be used to produce an animation of the simulation. The length, gravitational acceleration, initial angle, initial angular velocity and the position of the pivot can all be specified, all only on a 2D plane. The animation can be viewed and the initial conditions altered in a GUI, and the animation can be saved as an mp4 file. A brief demonstration:

https://github.com/user-attachments/assets/c15d6c70-d088-4e33-af1c-cc67aa637042

## Table of Contents

- [Pendulum](#pendulum)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [Testing](#testing)
    - [Updating GUI](#updating-gui)
    - [Updating Exectuable](#updating-exectuable)
  - [Contributing](#contributing)
  - [Contacts](#contacts)
  - [Licence](#licence)

## Setup

To install, clone the repository:
```shell
git clone https://github.com/LCrawford13/pendulum.git
```

It's recommended to use a fresh python environment, but if you're using an Anaconda Spyder environment, remove the PyQt5 and PyQt5-Qt5 dependencies from pyproject.toml, otherwise when running Spyder you'll get a "This application failed to start because no Qt platform plugin could be initialized." error.

Use poetry on the directory of the clone:
```shell
poetry install
```

If you get exit code status 9009, run this:
```shell
poetry config virtualenvs.use-poetry-python true
```

Note: I am unaware if this project will work on OS's other than Windows.

### Prerequisites

Python (>=3.12) is required.

Poetry is required, for the automatic installation of dependencies, https://python-poetry.org/docs/#installing-with-the-official-installer. 

If saving animations to mp4 files, then ffmpeg is needed: https://ffmpeg.org/download.html#build-windows.

## Usage

If you don't want to changed the code in any way, just download the latest release and go to pendulum/dist and run pendulum.exe.

Otherwise, it's best to run via an IDE, any python supported IDE will work. The file to run is src/main.py, it has a GUI, with all initial conditions having spin boxes to edit them. It can also be run in a terminal, at the project root directory, run `poetry run py src/main.py`.

src/txtMain.py also has a text-based user interface, or if desired, you can just change the values in an editor. txtMain.py isn't supported anymore, but it can be useful when doing minor tests. Running from the terminal can be done, via `poetry run py src/txtMain.py`, run from the root. However, if saving the animation to a file, then the pop-up window with the animation fails to appear, while if not saving to a file, the pop-up window will appear but the terminal will hang, meaning you will have to restart the terminal to run the program again.

Picture of animation pop-up window:

<img width="499" height="578" alt="window" src="https://github.com/user-attachments/assets/4bf0c436-5514-4a6d-9c28-046f82f8cc4a" />

Video of full animation on default settings:

https://github.com/user-attachments/assets/7d327dd5-6e8c-417a-903d-128b8165b4df

### Testing

Pytest is used for testing, just run `poetry run pytest` at the project directory, this will run all unit tests.

### Updating GUI

In a terminal go to the project directory/src, then run `pyuic5 -o ui_gui.py gui.ui`.

### Updating Exectuable

In a terminal, from the project directory run `poetry run pyinstaller pendulum.spec`.

## Contributing

Contributions aren't excepted at this time.

## Contacts

Github: [LCrawford13](https://github.com/LCrawford13)

## Licence

[Under MIT licence.](LICENCE)
