import time
import random
from sense_hat import SenseHat
from settings import *


class Snake_game:
    """
    Snake Game main class, with the game parameters, and methods.
    """

    def __init__(self):
        """
        Constructor of the Snake Game with the parameter of the Sense HAT panel and
        with the basic parameters of the snake like direction and
        the map parameters like apple position and pixels.
        """
        self.sense = SenseHat()
        self.trail = [[3, 3]]
        self.direction = [1, 0]  # x y
        self.length = 1
        self.apple_pos = [random.randint(0, 7), random.randint(0, 7)]
        self.pixels = [clear] * 64

    # 0 = up, 1 = right, 2 = down, 3 = left
    def set_direction(self, dir):
        """
        Snake Game direction setter, where set the snake moving direction.
        """
        if dir == 0:
            self.direction = [0, -1]
        elif dir == 1:
            self.direction = [1, 0]
        elif dir == 2:
            self.direction = [0, 1]
        elif dir == 3:
            self.direction = [-1, 0]

    # game loop
    def play_game(self):
        """
        Main loop of the game with the direction event handler, plus
        with the map border settings, movements and apple generator.
        """

        while True:
            self.pixels = [clear] * 64

            # sense HAT controller
            for event in self.sense.stick.get_events():
                if event.action == "pressed":
                    if event.direction == "up":
                        self.set_direction(0)
                    elif event.direction == "right":
                        self.set_direction(1)
                    elif event.direction == "down":
                        self.set_direction(2)
                    elif event.direction == "left":
                        self.set_direction(3)
            # insert to the start of the array
            self.trail.insert(0, [self.trail[0][0] + self.direction[0], self.trail[0][1] + self.direction[1]])

            # one border cross in and the other off
            if self.trail[0][0] < 0:
                self.trail[0][0] = 7
            if self.trail[0][1] < 0:
                self.trail[0][1] = 7
            if self.trail[0][0] > 7:
                self.trail[0][0] = 0
            if self.trail[0][1] > 7:
                self.trail[0][1] = 0

            # we cover the situation, when the apple pos is a snake pos in this if statement
            if self.trail[0] == self.apple_pos:
                self.apple_pos = []
                while self.apple_pos == []:
                    self.apple_pos = [random.randint(0, 7), random.randint(0, 7)]
                    if self.apple_pos in self.trail:
                        self.apple_pos = []
                self.length += 1
            # snake runs into itself
            elif self.trail[0] in self.trail[1:]:
                self.length = 1
            else:
                while len(self.trail) > self.length:
                    # remove from the end ( "like" moving, but the length is correct)
                    self.trail.pop()

            for pos in self.trail:
                # snake visualize on the pixel map (2d coord to 1d coord)
                self.pixels[pos[1] * 8 + pos[0]] = white

            # y * rowSize + x -> coordinate convert because of the pixel map
            self.pixels[self.apple_pos[1] * 8 + self.apple_pos[0]] = red
            # apple position (red led)
            self.sense.set_pixels(self.pixels)

            time.sleep(0.15)
