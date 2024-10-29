# QwSTPad Micropython Examples <!-- omit in toc -->

These are micropython examples for the Pimoroni [QwSTPad](https://shop.pimoroni.com/products/qwstpad), an I2C gamepad controller breakout.

- [Function Examples](#function-examples)
  - [Read All](#read-all)
  - [LED Wave](#led-wave)
  - [Pad Detect](#pad-detect)
- [Game Examples](#game-examples)
  - [Random Maze](#random-maze)
  - [Multi-Player](#multi-player)


## Function Examples

### Read All
[function/read_all.py](function/read_all.py)

How to read all of the buttons on QwSTPad.


### LED Wave
[function/led_wave.py](function/led_wave.py)

Apply a wave effect across QwSTPad's onboard LEDs.


### Pad Detect
[function/pad_detect.py](function/pad_detect.py)

How to detect multiple QwSTPads and handle their unexpected connection and disconnection.


## Game Examples

### Random Maze
[games/random_maze.py](games/random_maze.py)

A single player QwSTPad game demo. Navigate a set of mazes from the start (red) to the goal (green).
Mazes get bigger / harder with each increase in level.
Makes use of 1 QwSTPad and a Pico Display Pack 2.0 / 2.8.


### Multi-Player
[games/multi_player.py](games/multi_player.py)

A multi-player QwSTPad game demo. Each player drives a tank-like vehicle around an arena
with the goal of hitting other players with projects to get the most points.
Makes use of 1 to 4 QwSTPads and a Pico Display Pack 2.0 / 2.8.