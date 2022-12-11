# Pygame Dungeon Crawler
<p align="center">
    <img width="1000" src="https://github.com/luk27182/PyGame-Dungeon-Crawler/blob/main/Game_Preview.gif" alt="Gameplay Preview">
</p>


Demonstration video: [link]()


## Required Packages
Requirements:
- Python 3.10.9
- PyGame 2.1.2
### Python Instillation
First, you need to make sure that you have Python installed on your computer. These instructions will be for Windows as that is the type of computer that I have access to run tests on, but you can read [here](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/) for instructions on Python installation for other OSes, as well as alternative instructions for the Windows installation. 

To install Python 3.10.9 on Windows, first download the correct installer (dependent on your system) from [the official Python website](https://www.python.org/downloads/windows/). Then follow the prompts to install python on your computer.

You can test if Python is installed correctly on Windows by running the command
> python --version

in the command prompt. You should see the response
> Python 3.10.9

### Pip Installation
To install the PyGame package, we will use the pip installer. This is a common installer for installing Python packages. As before, I will only detail instructions for the Windows installation, but you can find instructions for other operating systems (as well as alternative instructions for the Windows installation) [here](https://www.geeksforgeeks.org/download-and-install-pip-latest-version/).

To install pip on Windows, first download the [get-pip.py file](https://bootstrap.pypa.io/get-pip.py) and store it in the same directory as where Python is installed. Then in the command line, change the directory until you are in the same folder as the get-pip.py file is located. Then, in the command line, enter the prompt
> python get-pip.py

Which executes the get-pip.py file. After this, pip will be installed on your computer. To test if installation was successful, run the command
> pip --version

and ensure that the response is of the form
> pip [version] from [file location] (python 3.10)

### PyGame Installation
With pip in place, it is easy to install PyGame. In the command prompt, simply run the command 
> pip install pygame

To check to make sure pygame is installed correctly, run the following command in the command prompt:
> pip show pygame

The response should give a detailed summary of the PyGame package you have installed. In particular, you should see the line
> Version: 2.1.2

neat the top of the response.

## Running the Game
To run the game, first download all files in this repository to your computer. Then navigate in the command prompt until your file path is the folder in which main.py is located. Finally, run the command
> python main.py

in the command prompt. The game should boot up in a separate window in full-screen.

## Playing the Game
The controls for the game are as follows:
- Player movement is with the keyboard's arrow keys or with WASD. Either work.
- The crosshair is controlled via mouse movement.
- Shoot, simply click the mouse.

## Resources
- Free [sound effects](https://opengameart.org/content/512-sound-effects-8-bit-style) by user SubspaceAudio [Juhani Junkala](https://juhanijunkala.com/)

- All art by me using [Piskel](https://www.piskelapp.com/) free pixel art app

- I learned PyGame by following the YouTuber [Clear Code's](https://www.youtube.com/@ClearCode) excellent tutorials. In particular, I used the code for collisions, importing folders, and player-following-camera from their [Zelda-Style Game Tutorial](https://www.youtube.com/watch?v=cwWi05Icpw0) and got the base code for the crosshair sprite from [a video in their PyGame Fundamentals series.](https://www.youtube.com/watch?v=hDu8mcAlY4E&list=PL8ui5HK3oSiHnIdi0XIAVXHAeulNmBrLy&index=2)
- I found GeeksForGeeks [page on working with CSV files in Python](https://www.geeksforgeeks.org/working-csv-files-python/) to be extremely helpful for implementing a leaderboard that interacted with a CSV file.
- Finally, I note that I used some code from [this stack overflow answer](https://stackoverflow.com/questions/14111381/how-to-get-text-input-from-user-in-pygame) as a base to implement a screen that allows the user to type in their name to the screen using PyGame.

## Design

See [DESIGN.MD](https://github.com/luk27182/PyGame-Dungeon-Crawler/blob/main/DESIGN.md) for a more in depth explanation of the design challenges I worked through to create this project.
