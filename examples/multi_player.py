import math

from machine import I2C
from picographics import DISPLAY_PICO_DISPLAY_2, PEN_RGB565, PicoGraphics

from qwstpad import ADDRESSES, QwSTPad

# Colour Constants
WHITE = const(65535)
BLACK = const(0)
CYAN = const(65287)
MAGENTA = const(8184)
YELLOW = const(57599)
GREEN = const(57351)
RED = const(248)
BLUE = const(7936)

# Projectile Constants
PROJECTILE_LIMIT = 15
PROJECTILE_SPEED = 5

# Player Constants
POSITIONS = ((30, 50), (280, 50), (30, 200), (280, 200))
COLOURS = (GREEN, MAGENTA, CYAN, BLUE)
LINE_LENGTH = 25
START_ANGLE = 20
PLAYER_RADIUS = 10
PLAYER_SPEED = 4

GRID_SPACING = 20


# Classes
class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def update(self):
        self.x += PROJECTILE_SPEED * math.cos(self.direction)
        self.y += PROJECTILE_SPEED * math.sin(self.direction)

    def draw(self, display):
        display.pixel(int(self.x), int(self.y))

    def is_on_screen(self):
        return self.x >= 0 and self.x < WIDTH and  self.y >= 0 and self.y < HEIGHT

    def has_hit(self, player):
        xdiff = self.x - player.x
        ydiff = self.y - player.y

        sqdist = xdiff ** 2 + ydiff ** 2
        return sqdist < player.size ** 2


class Player:
    def __init__(self, index, x, y, size, colour, pad):
        self.index = index
        self.x = x
        self.y = y
        self.direction = math.radians(START_ANGLE)
        self.size = size
        self.colour = colour
        self.pad = pad

        self.projectiles = []
        self.was_hit = False
        self.score = 0

    def fire(self):
        if len(self.projectiles) < PROJECTILE_LIMIT:
            self.projectiles.append(Projectile(self.x, self.y, self.direction))

    def update(self):
        # Read the player's gamepad
        button = self.pad.read_buttons()

        if button['L']:
            self.direction -= 0.1

        if button['R']:
            self.direction += 0.1

        if button['U']:
            self.x += PLAYER_SPEED * math.cos(self.direction)
            self.y += PLAYER_SPEED * math.sin(self.direction)

        if button['D']:
            self.x -= PLAYER_SPEED * math.cos(self.direction)
            self.y -= PLAYER_SPEED * math.sin(self.direction)

        if button['A']:
            self.fire()

        # Clamp the player to the screen area
        self.x = min(max(self.x, self.size), WIDTH - self.size)
        self.y = min(max(self.y, self.size), HEIGHT - self.size)

        new_proj = []
        for projectile in self.projectiles:
            projectile.update()
            if projectile.is_on_screen():
                new_proj.append(projectile)

        self.projectiles = new_proj

    def draw(self, display):
        x, y = int(self.x), int(self.y)
        display.set_pen(WHITE)
        display.circle(x, y, self.size)
        display.set_pen(BLACK) if not self.was_hit else display.set_pen(RED)
        display.circle(x, y, self.size - 1)
        self.was_hit = False

        # Draw the direction line in our colour
        display.set_pen(self.colour)
        display.line(x, y,
                     int(self.x + (LINE_LENGTH * math.cos(self.direction))),
                     int(self.y + (LINE_LENGTH * math.sin(self.direction))))

        # Draw the projectiles in our colour
        display.set_pen(self.colour)
        for p in self.projectiles:
            p.draw(display)

        # Draw our score at the bottom of the screen
        display.set_pen(self.colour)
        display.text(f"P{self.index + 1}: {self.score}", 5 + self.index * 80, 227, WIDTH, 2)


class Game(object):
    def __init__(self, i2c):
        self.players = []

        # Create a player for each QwSTPad detected
        for i in range(len(ADDRESSES)):
            try:
                player = Player(i, *(POSITIONS[i]), PLAYER_RADIUS, COLOURS[i], QwSTPad(i2c, ADDRESSES[i]))
                self.players.append(player)
                print(f"P{i + 1}: Connected")
            except OSError:
                print(f"P{i + 1}: Not Connected")

    def draw(self, display):
        # Clear the screen
        display.set_pen(BLACK)
        display.clear()

        # Draw a grid for the background
        display.set_pen(GREY)
        for x in range(0, WIDTH, GRID_SPACING):
            for y in range(0, HEIGHT, GRID_SPACING):
                display.pixel(x, y)

        # Draw players
        for p in self.players:
            p.draw(display)

        # Update the screen
        display.update()

    def update(self):
        # Update all players and projectiles to their new positions
        for p in self.players:
            p.update()

        # Check if any projectiles have hit players
        for p1 in self.players:
            for p2 in self.players:
                if p2 is not p1:
                    for projectile in p1.projectiles:
                        if projectile.has_hit(p2):
                            p2.was_hit = True
                            p1.score += 1


# Variables
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB565)
display.set_backlight(1.0)

WIDTH, HEIGHT = display.get_bounds()
GREY = display.create_pen(115, 115, 115)

i2c = I2C(0, scl=5, sda=4)
g = Game(i2c)

while True:
    g.update()
    g.draw(display)
