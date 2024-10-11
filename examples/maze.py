import time
from machine import I2C
from qwstpad import QwSTPad, DEFAULT_ADDRESS
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565

# Constants
WHITE = const(65535)
BLACK = const(0)
GREEN = const(57351)

# Classes

class Game(object):
    def __init__(self, i2c):

        self.complete = False

        # The square the player must get to.
        self.end_location = (1, 30)

        # Our maze, 1's are solid walls and 0's are the path we can move along.
        # Try changing some 1s and 0s and see how the maze changes! :)

        self.maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                     [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # Store the player pad objects
        self.pad = QwSTPad(i2c, address=DEFAULT_ADDRESS)

        # Our player object. Stores the current location and the colour of the player square.
        self.player = Player(1, 21, PLAYER)

    def draw(self, display):

        # Clear the screen
        display.set_pen(PATH)
        display.clear()
        display.set_pen(WHITE)

        # Draw the maze we have stored above.
        # Each '1' in the array is drawn as a 10x10 pixel square.
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                if self.maze[row][col] == 1:
                    display.set_pen(BLACK)
                    display.rectangle(col * 10 + 2, row * 10 + 2, 10, 10)
                    display.set_pen(WALL)
                    display.rectangle(col * 10, row * 10, 9, 9)

                if self.maze[row][col] == 2:
                    display.set_pen(GREEN)
                    display.rectangle(col * 10, row * 10, 9, 9)
                    display.set_pen(WALL)

        # Draw the player.
        display.set_pen(self.player.colour)
        display.rectangle(self.player.x * 10, self.player.y * 10, self.player.size - 1, self.player.size - 1)

        # Draw the end location square
        display.set_pen(GREEN)
        display.rectangle(self.end_location[1] * 10, self.end_location[0] * 10, 9, 9)

        if self.complete:
            # Draw banner shadow
            display.set_pen(BLACK)
            display.rectangle(4, 94, WIDTH, 50)
            # Draw banner
            display.set_pen(PLAYER)
            display.rectangle(0, 90, WIDTH, 50)

            # Draw text shadow
            display.set_pen(BLACK)
            display.text("Maze Complete!", WIDTH // 6 + 2, 107, WIDTH, 3)

            # Draw text
            display.set_pen(WHITE)
            display.text("Maze Complete!", WIDTH // 6, 105, WIDTH, 3)

        # Update the screen
        display.update()

    def update(self):

        button = self.pad.read_buttons()

        if button['L']:
            if self.maze[self.player.y][self.player.x - 1] == 0:
                self.player.x -= 1
                time.sleep(0.1)

        if button['R']:
            if self.maze[self.player.y][self.player.x + 1] == 0:
                self.player.x += 1
                time.sleep(0.1)

        if button['U']:
            if self.maze[self.player.y - 1][self.player.x] == 0:
                self.player.y -= 1
                time.sleep(0.1)

        if button['D']:
            if self.maze[self.player.y + 1][self.player.x] == 0:
                self.player.y += 1
                time.sleep(0.1)

        if self.player.x == self.end_location[1] and self.player.y == self.end_location[0]:
            self.complete = True


class Player(object):
    # The player object.
    # Stores the current location of the player in the maze.
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.size = 10
        self.colour = colour


display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB565)
display.set_backlight(1.0)

WIDTH, HEIGHT = display.get_bounds()

# Set some colours to use later.
WALL = display.create_pen(127, 125, 244)
PATH = display.create_pen(60, 57, 169)
PLAYER = display.create_pen(227, 231, 110)

display.set_pen(BLACK)
display.clear()


i2c = I2C(0, scl=5, sda=4)
g = Game(i2c)

while True:
    if not g.complete:
        g.update()
    g.draw(display)