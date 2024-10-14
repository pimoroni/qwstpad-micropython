import math

from machine import I2C
from picographics import DISPLAY_PICO_DISPLAY_2, PEN_RGB565, PicoGraphics

from qwstpad import ADDRESSES, QwSTPad

# Constants
WHITE = const(65535)
BLACK = const(0)
CYAN = const(65287)
MAGENTA = const(8184)
YELLOW = const(57599)
GREEN = const(57351)
RED = const(248)
BLUE = const(7936)


# Classes
class Projectile(object):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def update(self):
        self.x += int(5 * math.cos(self.direction))
        self.y += int(5 * math.sin(self.direction))


class Game(object):
    def __init__(self, i2c):
        self.player = [Player(30, 50, 10, GREEN), Player(280, 50, 10, MAGENTA),
                       Player(30, 200, 10, CYAN), Player(280, 200, 10, BLUE)]

        # Store the player pad objects
        self.pad = [QwSTPad(i2c, address=ADDRESSES[0]),
                    QwSTPad(i2c, address=ADDRESSES[1]),
                    QwSTPad(i2c, address=ADDRESSES[2]),
                    QwSTPad(i2c, address=ADDRESSES[3])]

        self.xmin = 10
        self.xmax = WIDTH
        self.ymin = 10
        self.ymax = HEIGHT
        self.winner = False

    def draw(self, display):

        # Clear the screen
        display.set_pen(BLACK)
        display.clear()

        # Draw a grid for the background
        display.set_pen(GREY)
        for x in range(0, WIDTH, 20):
            for y in range(0, HEIGHT, 20):
                display.pixel(x, y)

        # Draw players
        for p in self.player:
            display.set_pen(WHITE)
            display.circle(p.x, p.y, p.size)
            display.set_pen(BLACK) if not p.was_hit else display.set_pen(RED)
            display.circle(p.x, p.y, p.size - 1)
            p.was_hit = False
            display.set_pen(p.colour)
            display.line(p.x, p.y, int(p.x + (p.line_length * math.cos(p.direction))), int(p.y + (p.line_length * math.sin(p.direction))))

            for i in p.projectiles:
                display.set_pen(p.colour)
                display.pixel(i.x, i.y)

            for i, p in enumerate(self.player):
                display.set_pen(p.colour)
                display.text(f"P{i + 1}: {p.score}", 5 + i * 80, 227, WIDTH, 2)

        # Update the screen
        display.update()

    def update(self):
        for i, p in enumerate(self.pad):

            button = p.read_buttons()

            if button['L']:
                self.player[i].direction -= 0.1

            if button['R']:
                self.player[i].direction += 0.1

            if button['U']:
                self.player[i].x += int(5 * math.cos(self.player[i].direction))
                self.player[i].y += int(5 * math.sin(self.player[i].direction))

            if button['D']:
                self.player[i].x -= int(5 * math.cos(self.player[i].direction))
                self.player[i].y -= int(5 * math.sin(self.player[i].direction))

            if button['A']:
                self.player[i].new_projectile()

            self.player[i].x = min(self.player[i].x, self.xmax - self.player[i].size)
            self.player[i].x = max(self.player[i].x, self.xmin + self.player[i].size)

            self.player[i].y = min(self.player[i].y, self.ymax - self.player[i].size)
            self.player[i].y = max(self.player[i].y, self.ymin + self.player[i].size)

        for p in self.player:
            p.update()

        for i, p in enumerate(self.player):
            for j in range(len(self.player)):
                if not i == j:
                    p2 = self.player[j]

                    for projectile in p.projectiles:

                        xdif = projectile.x - p2.x
                        ydif = projectile.y - p2.y

                        sqdist = xdif ** 2 + ydif ** 2

                        if sqdist < p2.size ** 2:
                            p2.was_hit = True
                            p.score += 1


class Player(object):
    def __init__(self, x, y, size, colour):
        self.direction = math.radians(20)
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.line_length = 25
        self.projectiles = []
        self.was_hit = False
        self.score = 0

    def new_projectile(self):
        if len(self.projectiles) < 15:
            self.projectiles.append(Projectile(self.x, self.y, self.direction))

    def update(self):
        if self.projectiles:
            new_proj = []
            for i, projectile in enumerate(self.projectiles):
                projectile.update()
                if projectile.x > WIDTH or projectile.x < 0 or projectile.y < 0 or projectile.y > HEIGHT:
                    pass
                else:
                    new_proj.append(projectile)
            self.projectiles = new_proj


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
